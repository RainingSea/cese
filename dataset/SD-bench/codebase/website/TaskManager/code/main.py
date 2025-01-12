from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from task import Task
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = {}
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password, email = line.strip().split('|')
                users[username] = User(username, password, email)
    return users

users = load_users()

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
        users[username] = new_user
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    current_user = session['username']
    task_manager = Task()
    
    if request.method == 'POST':
        if 'add_task' in request.form:
            task_description = request.form['task_description']
            due_date = request.form['due_date']
            task_manager = Task(task_description, due_date)
            task_manager.save(current_user)
        elif 'remove_task' in request.form:
            task_index = int(request.form['task_index'])
            task_manager.remove_task(current_user, task_index)

    tasks = task_manager.load_tasks(current_user)
    return render_template('home.html', tasks=tasks)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username].password == password:
        session['username'] = username
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8313, debug=False)
