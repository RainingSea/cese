from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

class Task:
    def __init__(self, description: str, due_date: str):
        self.description = description
        self.due_date = due_date

    def save(self, username: str):
        with open(f'tasks_{username}.txt', 'a') as f:
            f.write(f"{self.description}|{self.due_date}\n")

    def remove(self, username: str):
        tasks = self.load(username)
        tasks = [task for task in tasks if task.description != self.description]
        with open(f'tasks_{username}.txt', 'w') as f:
            for task in tasks:
                f.write(f"{task.description}|{task.due_date}\n")

    @staticmethod
    def load(username: str) -> list:
        tasks = []
        if os.path.exists(f'tasks_{username}.txt'):
            with open(f'tasks_{username}.txt', 'r') as f:
                for line in f:
                    description, due_date = line.strip().split('|')
                    tasks.append(Task(description, due_date))
        return tasks

class UserManager:
    def register(self, username: str, password: str, email: str) -> bool:
        users = self.load_users()
        if any(user.username == username for user in users):
            return False
        user = User(username, password, email)
        user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        users = self.load_users()
        return any(user.username == username and user.password == password for user in users)

    def load_users(self) -> list:
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        return users

class TaskManager:
    def load_tasks(self, username: str) -> list:
        return Task.load(username)

    def add_task(self, username: str, description: str, due_date: str):
        task = Task(description, due_date)
        task.save(username)

    def remove_task(self, username: str, description: str):
        task = Task(description, "")
        task.remove(username)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager = UserManager()
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/home')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user_manager = UserManager()
        if user_manager.register(username, password, email):
            return redirect('/')
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    task_manager = TaskManager()
    tasks = task_manager.load_tasks(username)
    if request.method == 'POST':
        description = request.form['description']
        due_date = request.form['due_date']
        task_manager.add_task(username, description, due_date)
        return redirect('/home')
    return render_template('home.html', tasks=tasks)

@app.route('/remove_task', methods=['POST'])
def remove_task():
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    description = request.form['description']
    task_manager = TaskManager()
    task_manager.remove_task(username, description)
    return redirect('/home')

if __name__ == '__main__':
    app.run(port=8076, debug=False)
