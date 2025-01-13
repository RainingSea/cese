from flask import Flask, render_template, request, redirect, url_for, session
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
        self.users = {}
        self.tasks = {}

        self.load_users()

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = User(username, password, email)
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        return user is not None and user.password == password

    def add_task(self, username: str, task_description: str, due_date: str) -> bool:
        if username not in self.tasks:
            self.tasks[username] = []
        self.tasks[username].append((task_description, due_date))
        self.save_tasks(username)
        return True

    def remove_task(self, username: str, task_index: int) -> bool:
        if username in self.tasks and 0 <= task_index < len(self.tasks[username]):
            del self.tasks[username][task_index]
            self.save_tasks(username)
            return True
        return False

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split(',')
                    self.users[username] = User(username, password, email)

    def load_tasks(self, username: str):
        if os.path.exists(f'tasks_{username}.txt'):
            with open(f'tasks_{username}.txt', 'r') as file:
                self.tasks[username] = [tuple(line.strip().split(',')) for line in file]

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users.values():
                file.write(f"{user.username},{user.password},{user.email}\n")

    def save_tasks(self, username: str):
        with open(f'tasks_{username}.txt', 'w') as file:
            for task in self.tasks.get(username, []):
                file.write(f"{task[0]},{task[1]}\n")

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
    username = session.get('username')
    if username is None:
        return redirect(url_for('login'))

    if request.method == 'POST':
        task_description = request.form['task_description']
        due_date = request.form['due_date']
        task_manager.add_task(username, task_description, due_date)

    tasks = task_manager.tasks.get(username, [])
    return render_template('home.html', tasks=tasks)

@app.route('/remove_task/<int:task_index>', methods=['POST'])
def remove_task(task_index):
    username = session.get('username')
    if username is not None:
        task_manager.remove_task(username, task_index)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=8498, debug=False)
