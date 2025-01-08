from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from task import Task
from task_manager import TaskManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production
task_manager = TaskManager()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if task_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('task_home'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if task_manager.register(username, password, email):
            return redirect(url_for('login'))
        else:
            return "Registration failed. Username may already exist."
    return render_template('register.html')

@app.route('/task_home')
def task_home():
    if 'username' not in session:
        return redirect(url_for('login'))
    tasks = task_manager.get_tasks(session['username'])
    return render_template('home.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'username' not in session:
        return redirect(url_for('login'))
    description = request.form['description']
    due_date = request.form['due_date']
    task_manager.add_task(session['username'], description, due_date)
    return redirect(url_for('task_home'))

@app.route('/delete_task/<int:task_index>')
def delete_task(task_index):
    if 'username' not in session:
        return redirect(url_for('login'))
    task_manager.delete_task(session['username'], task_index)
    return redirect(url_for('task_home'))

if __name__ == '__main__':
    app.run(port=8344, debug=False)
