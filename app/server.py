from flask import Flask, render_template, jsonify

# Данные задач
Tasks = [{
    "name": "Task 1",
    "starting_date": "12.11.2024",
    "ending_date": "13.11.2024",
    "is_complete": False,
    "description": "qweqwe"
},
{
    "name": "Task 2",
    "starting_date": "01.12.2024",
    "ending_date": "02.11.2024",
    "is_complete": True,
    "description": "asdasd"
}]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', tasks=Tasks)

@app.route('/tasks_json')
def tasks_json():
    return jsonify(Tasks)

