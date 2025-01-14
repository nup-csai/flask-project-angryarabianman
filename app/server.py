from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db = SQLAlchemy(app)

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
    starting_date = db.Column("starting_date", db.DateTime)
    ending_date = db.Column("ending_date", db.DateTime)
    is_task_complete = db.Column("task_status", db.Boolean)

    def __init__(self, user_email, name, description, starting_date, ending_date, is_task_complete):
        self.user_email = user_email
        self.name = name
        self.description = description
        self.starting_date = starting_date
        self.ending_date = ending_date
        self.is_task_complete = is_task_complete

db.create_all()
@app.route('/', methods=['GET', 'POST'])
def home():
    email = "none"
    tasks_list = []
    if "logged_in" in session:
        email = session['email']
        tasks_list = tasks.query.filter_by(user_email=email).all()
    return render_template('index.html', email=email, tasks=tasks_list)

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
            user = users(email, password)
            db.session.add(user)
            db.session.commit()

        return redirect(url_for('home'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        found_user = users.query.filter_by(email=email).first()

        if found_user:
            if found_user.password == password:
                session['logged_in'] = True
                session['email'] = email
                session['password'] = password
                session['tasks'] = tasks.query.filter_by(user_email=email).all()
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
        session.pop('password', None)
        session.pop('tasks', None)
    return redirect(url_for('home'))
@app.route('/add_task')
def add_task():
    if 'logged_in' in session:
        user_email = session['email']
        name = "Name"
        description = "Description"
        starting_date = datetime.now()
        ending_date = starting_date
        is_task_complete = False
        print(123)
        task = tasks(user_email, name, description, starting_date, ending_date, is_task_complete)
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('home'))
