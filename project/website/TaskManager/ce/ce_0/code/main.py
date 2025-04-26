from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

class UserManager:
    def __init__(self, filename):
        self.filename = filename
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    self.users[username] = (password, email)

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        self.users[username] = (password, email)
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username][0] == password:
            session['username'] = username
            return True
        return False

class TaskManager:
    def __init__(self, filename):
        self.filename = filename
        self.load_tasks()

    def load_tasks(self):
        self.tasks = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    description, due_date = line.strip().split('|')
                    self.tasks.append((description, due_date))

    def add_task(self, description: str, due_date: str) -> bool:
        with open(self.filename, 'a') as file:
            file.write(f"{description}|{due_date}\n")
        self.tasks.append((description, due_date))
        return True

    def remove_task(self, task_id: int) -> bool:
        if 0 <= task_id < len(self.tasks):
            del self.tasks[task_id]
            self.save_tasks()
            return True
        return False

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            for description, due_date in self.tasks:
                file.write(f"{description}|{due_date}\n")

    def get_tasks(self) -> list:
        return self.tasks

user_manager = UserManager('users.txt')
task_manager = TaskManager('tasks.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect('/home')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect('/')
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        if 'add_task' in request.form:
            description = request.form['description']
            due_date = request.form['due_date']
            task_manager.add_task(description, due_date)
        elif 'remove_task' in request.form:
            task_id = int(request.form['task_id'])
            task_manager.remove_task(task_id)
    tasks = task_manager.get_tasks()
    return render_template('home.html', tasks=tasks)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8254, debug=False)
