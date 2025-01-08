from flask import Flask, render_template, request, redirect, session
from user import User
from task import Task
from task_manager import TaskManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
task_manager = TaskManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if task_manager.login(username, password):
            session['username'] = username
            return redirect('/home')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if task_manager.register(username, password, email):
            return redirect('/')
        else:
            return "Registration failed"
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def task_home():
    if 'username' not in session:
        return redirect('/')
    tasks = task_manager.get_tasks(session['username'])
    return render_template('home.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'username' not in session:
        return redirect('/')
    description = request.form['description']
    due_date = request.form['due_date']
    task_manager.add_task(session['username'], description, due_date)
    return redirect('/home')

@app.route('/delete_task/<int:task_index>', methods=['POST'])
def delete_task(task_index):
    if 'username' not in session:
        return redirect('/')
    task_manager.delete_task(session['username'], task_index)
    return redirect('/home')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8345, debug=False)
