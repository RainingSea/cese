from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from task import Task
from datastore import DataStore
from task_manager import TaskManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
data_store = DataStore()
task_manager = TaskManager(data_store)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if task_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid credentials, please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if task_manager.register_user(username, password, email):
            return redirect(url_for('login'))
        else:
            return "Username already exists."
    return render_template('registration.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    username = session.get('username')
    if username is None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        task_description = request.form['task_description']
        due_date = request.form['due_date']
        task_manager.add_task(username, task_description, due_date)
    tasks = task_manager.get_tasks(username)
    return render_template('home.html', tasks=tasks, username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8499, debug=False)
