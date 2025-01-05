from flask import Flask, render_template, request, redirect, session
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
                    username, password, email = line.strip().split(',')
                    self.users[username] = User(username, password, email)

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users.values():
                file.write(f"{user.username},{user.password},{user.email}\n")

    def load_tasks(self, username: str) -> list:
        tasks = []
        filename = f'tasks_{username}.txt'
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                for line in file:
                    task_description, due_date = line.strip().split(',')
                    tasks.append((task_description, due_date))
        return tasks

    def save_tasks(self, username: str) -> None:
        filename = f'tasks_{username}.txt'
        with open(filename, 'w') as file:
            for task in self.tasks.get(username, []):
                file.write(f"{task[0]},{task[1]}\n")

    def add_task(self, username: str, task_description: str, due_date: str) -> None:
        if username not in self.tasks:
            self.tasks[username] = []
        self.tasks[username].append((task_description, due_date))
        self.save_tasks(username)

    def remove_task(self, username: str, task_index: int) -> None:
        if username in self.tasks and 0 <= task_index < len(self.tasks[username]):
            del self.tasks[username][task_index]
            self.save_tasks(username)

    def register_user(self, username: str, password: str, email: str) -> bool:
        if username not in self.users:
            self.users[username] = User(username, password, email)
            self.save_users()
            return True
        return False

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
            return redirect('/home')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if task_manager.register_user(username, password, email):
            return redirect('/')
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    if request.method == 'POST':
        task_description = request.form['task_description']
        due_date = request.form['due_date']
        task_manager.add_task(username, task_description, due_date)
    tasks = task_manager.load_tasks(username)
    return render_template('home.html', tasks=tasks)

@app.route('/remove_task/<int:task_index>', methods=['POST'])
def remove_task(task_index):
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    task_manager.remove_task(username, task_index)
    return redirect('/home')

if __name__ == '__main__':
    app.run(port=8114, debug=False)
