from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from task import Task
from task_manager import TaskManager
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
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
        task_manager.register(username, password, email)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    if request.method == 'POST':
        if 'add_task' in request.form:
            description = request.form['description']
            due_date = request.form['due_date']
            task_manager.add_task(username, description, due_date)
        elif 'delete_task' in request.form:
            task_index = int(request.form['task_index'])
            task_manager.delete_task(username, task_index)

    tasks = task_manager.get_tasks(username)
    return render_template('home.html', tasks=tasks)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    
    if task_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8343, debug=False)
