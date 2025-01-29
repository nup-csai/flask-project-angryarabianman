from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from datetime import timedelta, datetime
from flask_mail import Mail, Message
import logging
import smtplib, string, random
import os.path
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'ilya.task.manager@gmail.com'
app.config['MAIL_PASSWORD'] = 'mzwrvbnotfbqcklo'
app.config['MAIL_DEFAULT_SENDER'] = 'ilya.task.manager@gmail.com'

app.app_context().push()

SENDER_EMAIL = "ilya.task.manager@gmail.com"
SENDER_PASSWORD = "mzwrvbnotfbqcklo"

db = SQLAlchemy(app)
mail = Mail(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column("email", db.String)
    password = db.Column("password", db.String)
    def __init__(self, email, password):
        self.email = email
        self.password = password

class tasks(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)

    user_email = db.Column("user_email", db.String)
    name = db.Column("name", db.String)
    description = db.Column("description", db.String)
    ending_date = db.Column("ending_date", db.DateTime)
    is_task_complete = db.Column("task_status", db.Boolean)
    notification_sent = db.Column("notification_sent", db.Boolean)
    def __init__(self, user_email, name, description, ending_date, is_task_complete, notification_sent = False):
        self.user_email = user_email
        self.name = name
        self.description = description
        self.ending_date = ending_date
        self.is_task_complete = is_task_complete
        self.notification_sent = notification_sent

db.create_all()

def get_task_info():
    name = request.form.get("input_task_name")
    description = request.form.get("input_description")
    ending_date = datetime.strptime(request.form.get("input_ending_date"), '%Y-%m-%d')
    task = tasks(session["email"], name, description, ending_date, False)
    return task
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        task_id = request.form.get("task_id")
        action = request.form.get("action")
        if task_id and action:
            if action == "Delete task":
                task = tasks.query.get(task_id)
                db.session.delete(task)
                db.session.commit()
                return redirect(url_for('home'))

        if request.form.get("add_task"):
            task = get_task_info()
            db.session.add(task)
            db.session.commit()
            return redirect(url_for('home'))

        if request.form.get("edit_mode"):
            home.edit_mode = not home.edit_mode
            if home.edit_mode:
                session['name'] = request.form.get("input_task_name")
                session['description'] = request.form.get("input_description")
                session['ending_date'] = datetime.strptime(request.form.get("input_ending_date"), '%Y-%m-%d')
            else:
                session.pop('name')
                session.pop('description')
                session.pop('ending_date')
            return redirect(url_for('home'))

        if task_id and action == "Edit task":
            task = tasks.query.filter_by(_id=task_id).first()
            task.name = session['name']
            task.description = session['description']
            task.ending_date = session['ending_date']
            db.session.commit()
            home.edit_mode = not home.edit_mode
            return redirect(url_for('home'))

        if task_id and action == "Change status":
            task = tasks.query.filter_by(_id=task_id).first()
            task.is_task_complete = not task.is_task_complete
            db.session.commit()
            return redirect(url_for('home'))

        if request.form.get("show_completed"):
            home.show_completed = not home.show_completed
            return redirect(url_for('home'))

    if "logged_in" in session:
        email = session['email']
        tasks_list = tasks.query.filter_by(user_email=email).all()
        return render_template('index.html', email=email, tasks=tasks_list, edit_mode=home.edit_mode, show_completed=home.show_completed)
    else:
        return render_template('welcome.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        found_user = users.query.filter_by(email=email).first()

        if found_user:
            flash('Email already registered', 'error')
            return redirect(url_for('signup'))
        else:
            session['email'] = email
            session['password'] = password
            return redirect(url_for('verify'))

    return render_template('signup.html')

@app.route('/signup/verify', methods=['GET', 'POST'])
def verify():
    if request.method == "GET":
        session['code'] = ''.join([random.choice(string.ascii_uppercase +
                                               string.ascii_lowercase +
                                               string.digits)
                                 for n in range(6)])
        msg = Message(
            subject="Task manager authentication code",
            recipients=[session['email']],
            body=session['code']
        )
        mail.send(msg)

    if request.method == 'POST':
        user = users(session["email"], session["password"])
        code = session['code']
        session.clear()
        if request.form.get('code') == code:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

        return redirect(url_for('signup'))

    return render_template('verify.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        found_user = users.query.filter_by(email=email).first()

        if found_user and found_user.password == password:
                session['logged_in'] = True
                session['email'] = email
                return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
        session.pop('email', None)
    return redirect(url_for('home'))


home.edit_mode = False
home.show_completed = True

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

