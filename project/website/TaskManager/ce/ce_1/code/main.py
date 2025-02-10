from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a random secret key for production

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

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    self.users[username] = User(username, password, email)

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = User(username, password, email)
        self.save_data()
        return True

    def login(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        if user and user.password == password:
            return True
        return False

    def load_tasks(self, username: str) -> list:
        tasks_file = f'tasks_{username}.txt'
        if os.path.exists(tasks_file):
            with open(tasks_file, 'r') as file:
                return [line.strip() for line in file.readlines()]
        return []

    def add_task(self, username: str, description: str, due_date: str) -> bool:
        tasks_file = f'tasks_{username}.txt'
        with open(tasks_file, 'a') as file:
            file.write(f"{description}|{due_date}\n")
        return True

    def remove_task(self, username: str, task_id: int) -> bool:
        tasks_file = f'tasks_{username}.txt'
        tasks = self.load_tasks(username)
        if 0 <= task_id < len(tasks):
            del tasks[task_id]
            with open(tasks_file, 'w') as file:
                for task in tasks:
                    file.write(task + '\n')
            return True
        return False

    def save_data(self):
        with open('users.txt', 'w') as file:
            for user in self.users.values():
                file.write(f"{user.username}|{user.password}|{user.email}\n")

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
    
    username = session['username']
    tasks = task_manager.load_tasks(username)

    if request.method == 'POST':
        description = request.form['description']
        due_date = request.form['due_date']
        task_manager.add_task(username, description, due_date)
        return redirect(url_for('home'))

    return render_template('home.html', tasks=tasks)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8580, debug=False)
