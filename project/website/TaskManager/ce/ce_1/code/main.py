from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str) -> None:
        self.username = username
        self.password = password
        self.email = email

class TaskManager:
    def __init__(self):
        self.users = {}
        self.tasks = {}

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    self.users[username] = User(username, password, email)

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users.values():
                file.write(f"{user.username}|{user.password}|{user.email}\n")

    def load_tasks(self, username: str) -> list:
        tasks = []
        filename = f'tasks_{username}.txt'
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                for line in file:
                    task_description, due_date = line.strip().split('|')
                    tasks.append((task_description, due_date))
        return tasks

    def save_tasks(self, username: str) -> None:
        filename = f'tasks_{username}.txt'
        with open(filename, 'w') as file:
            for task in self.tasks.get(username, []):
                file.write(f"{task[0]}|{task[1]}\n")

    def add_task(self, username: str, task: str, due_date: str) -> None:
        if username not in self.tasks:
            self.tasks[username] = []
        self.tasks[username].append((task, due_date))
        self.save_tasks(username)

    def remove_task(self, username: str, task: str) -> None:
        if username in self.tasks:
            self.tasks[username] = [t for t in self.tasks[username] if t[0] != task]
            self.save_tasks(username)

    def register_user(self, username: str, password: str, email: str) -> None:
        self.users[username] = User(username, password, email)
        self.save_users()

    def authenticate_user(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        return user is not None and user.password == password

task_manager = TaskManager()
task_manager.load_users()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if task_manager.authenticate_user(username, password):
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        task_manager.register_user(username, password, email)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        task_description = request.form['task_description']
        due_date = request.form['due_date']
        task_manager.add_task(username, task_description, due_date)

    tasks = task_manager.load_tasks(username)
    return render_template('home.html', tasks=tasks)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8987, debug=False)
