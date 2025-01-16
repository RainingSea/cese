from flask import Flask, render_template, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

class TaskManager:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.email = ""

    def login(self, username: str, password: str) -> bool:
        users = self.load_user_data()
        if username in users and users[username] == password:
            self.username = username
            return True
        return False

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.load_user_data():
            return False
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}|{email}\n")
        return True

    def add_task(self, task_description: str, due_date: str) -> bool:
        tasks_file = f'tasks_{self.username}.txt'
        with open(tasks_file, 'a') as f:
            f.write(f"{task_description}|{due_date}\n")
        return True

    def remove_task(self, task_id: int) -> bool:
        tasks_file = f'tasks_{self.username}.txt'
        tasks = self.view_tasks()
        if 0 <= task_id < len(tasks):
            del tasks[task_id]
            with open(tasks_file, 'w') as f:
                for task in tasks:
                    f.write(f"{task}\n")
            return True
        return False

    def view_tasks(self) -> list:
        tasks_file = f'tasks_{self.username}.txt'
        if not os.path.exists(tasks_file):
            return []
        with open(tasks_file, 'r') as f:
            return [line.strip() for line in f.readlines()]

    def load_user_data(self) -> dict:
        users = {}
        if not os.path.exists('users.txt'):
            return users
        with open('users.txt', 'r') as f:
            for line in f:
                username, password, email = line.strip().split('|')
                users[username] = password
        return users

    def save_user_data(self) -> None:
        pass  # Not needed as we save directly to the file

task_manager = TaskManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if task_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
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
    if 'username' not in session:
        return redirect(url_for('login'))
    task_manager.username = session['username']
    if request.method == 'POST':
        if 'add_task' in request.form:
            task_description = request.form['task_description']
            due_date = request.form['due_date']
            task_manager.add_task(task_description, due_date)
        elif 'remove_task' in request.form:
            task_id = int(request.form['task_id'])
            task_manager.remove_task(task_id)
    tasks = task_manager.view_tasks()
    return render_template('home.html', tasks=tasks)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8495, debug=False)
