from flask import Flask, render_template, request, redirect, session
from user import User
from task import Task
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username, password, email)
        user.save()
        return redirect('/')
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect('/')
    
    username = session['username']
    task_manager = Task()
    
    if request.method == 'POST':
        if 'add_task' in request.form:
            description = request.form['description']
            due_date = request.form['due_date']
            task = Task(description, due_date)
            task.save(username)
        elif 'remove_task' in request.form:
            task_description = request.form['task_description']
            task_manager.remove_task(username, task_description)

    tasks = task_manager.load_tasks(username)
    return render_template('home.html', tasks=tasks)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User()
    users = user.load_users()
    
    for u in users:
        if u[0] == username and u[1] == password:
            session['username'] = username
            return redirect('/home')
    
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8155, debug=True)
