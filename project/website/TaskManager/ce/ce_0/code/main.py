import os
from flask import Flask, render_template, request, redirect, url_for, flash
from user_manager import UserManager
from task_manager import TaskManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

user_manager = UserManager('users.txt')
task_manager = TaskManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect(url_for('home', username=username))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username may already exist.')
    return render_template('registration.html')

@app.route('/home/<username>', methods=['GET', 'POST'])
def home(username):
    if request.method == 'POST':
        task_description = request.form['task_description']
        due_date = request.form['due_date']
        task_manager.add_task(username, task_description, due_date)
    tasks = task_manager.list_tasks(username)
    return render_template('home.html', tasks=tasks, username=username)

if __name__ == '__main__':
    app.run(port=8426, debug=False)
