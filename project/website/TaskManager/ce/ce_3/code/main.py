from flask import Flask, render_template, request, redirect, url_for, session
from typing import List
import os

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

class TaskManager:
    def __init__(self, users_file: str, tasks_file: str):
        self.users_file = users_file
        self.tasks_file = tasks_file
        self.users = self.load_users()
        self.tasks = self.load_tasks()

    def load_users(self) -> List[User]:
        users = []
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        return users

    def load_tasks(self) -> dict:
        tasks = {}
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as file:
                for line in file:
                    username, task_description, due_date = line.strip().split('|')
                    if username not in tasks:
                        tasks[username] = []
                    tasks[username].append((task_description, due_date))
        return tasks

    def register(self, username: str, password: str, email: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password, email)
        self.users.append(new_user)
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user.username == username and user.password == password for user in self.users)

    def add_task(self, username: str, task_description: str, due_date: str) -> None:
        if username not in self.tasks:
            self.tasks[username] = []
        self.tasks[username].append((task_description, due_date))
        with open(self.tasks_file, 'a') as file:
            file.write(f"{username}|{task_description}|{due_date}\n")

    def remove_task(self, username: str, task_id: int) -> None:
        if username in self.tasks and 0 <= task_id < len(self.tasks[username]):
            self.tasks[username].pop(task_id)

app = Flask(__name__)
app.secret_key = 'your_secret_key'
task_manager = TaskManager('users.txt', 'tasks.txt')

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
    username = session['username']
    if request.method == 'POST':
        task_description = request.form['task_description']
        due_date = request.form['due_date']
        task_manager.add_task(username, task_description, due_date)
    tasks = task_manager.tasks.get(username, [])
    return render_template('home.html', tasks=tasks)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8989, debug=False)
