from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from task import Task
from task_manager import TaskManager
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

task_manager = TaskManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if task_manager.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'add_task' in request.form:
            description = request.form['description']
            due_date = request.form['due_date']
            task_manager.add_task(session['username'], description, due_date)
        elif 'logout' in request.form:
            session.pop('username', None)
            return redirect(url_for('login'))
    tasks = task_manager.get_tasks(session['username'])
    return render_template('home.html', tasks=tasks)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if task_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('home'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8340, debug=False)
