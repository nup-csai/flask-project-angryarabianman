from flask import Flask, render_template, request, redirect, url_for, jsonify

Tasks = []
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
    return render_template('index.html', tasks=Tasks)

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        Tasks.append({
            'name': request.form['task_name'],
            'starting_date': request.form['starting_date'],
            'ending_date': request.form['ending_date'],
            'is_complete': False,
            'description': request.form['description']
        })
        return redirect(url_for('add_task'))

    return render_template('add_task_form.html')

@app.route('/tasks_json')
def tasks_json():
    return jsonify(Tasks)

