from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self, filename='users.txt'):
        self.filename = filename
        self.users = self.load_users()

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        with open(self.filename, 'a') as f:
            f.write(f"{username}|{password}|{email}\n")
        self.users[username] = (password, email)
        return True

    def login(self, username: str, password: str) -> bool:
        return username in self.users and self.users[username][0] == password

    def load_users(self) -> dict:
        users = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    users[username] = (password, email)
        return users

class TaskManager:
    def __init__(self, username: str):
        self.filename = f'tasks_{username}.txt'
        self.tasks = self.load_tasks()

    def add_task(self, description: str, due_date: str) -> bool:
        task_id = len(self.tasks) + 1
        with open(self.filename, 'a') as f:
            f.write(f"{task_id}|{description}|{due_date}\n")
        self.tasks.append((task_id, description, due_date))
        return True

    def remove_task(self, task_id: int) -> bool:
        self.tasks = [task for task in self.tasks if task[0] != task_id]
        self.save_tasks()
        return True

    def load_tasks(self) -> list:
        tasks = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                for line in f:
                    task_id, description, due_date = line.strip().split('|')
                    tasks.append((int(task_id), description, due_date))
        return tasks

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            for task in self.tasks:
                f.write(f"{task[0]}|{task[1]}|{task[2]}\n")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager = UserManager()
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home', username=username))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user_manager = UserManager()
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
        else:
            flash('Username already exists')
    return render_template('registration.html')

@app.route('/home/<username>', methods=['GET', 'POST'])
def home(username):
    if 'username' not in session or session['username'] != username:
        return redirect(url_for('login'))
    
    task_manager = TaskManager(username)
    if request.method == 'POST':
        if 'add_task' in request.form:
            description = request.form['description']
            due_date = request.form['due_date']
            task_manager.add_task(description, due_date)
        elif 'remove_task' in request.form:
            task_id = int(request.form['task_id'])
            task_manager.remove_task(task_id)
    return render_template('home.html', tasks=task_manager.tasks)

if __name__ == '__main__':
    app.run(port=8429, debug=False)
