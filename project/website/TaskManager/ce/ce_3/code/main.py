from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from task import Task
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    task_manager = Task()
    
    if request.method == 'POST':
        if 'add_task' in request.form:
            description = request.form['description']
            due_date = request.form['due_date']
            new_task = Task(description, due_date)
            new_task.save(username)
        elif 'remove_task' in request.form:
            task_id = int(request.form['task_id'])
            task_manager.remove_task(username, task_id)
    
    tasks = task_manager.load_tasks(username)
    return render_template('home.html', tasks=tasks)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = User().load_users()
    
    for user in users:
        if user[0] == username and user[1] == password:
            session['username'] = username
            return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8582, debug=False)
