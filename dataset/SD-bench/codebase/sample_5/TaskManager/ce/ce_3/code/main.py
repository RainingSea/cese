from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key in production

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

    @staticmethod
    def load(username: str):
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1], user_data[2])
        return None

class Task:
    def __init__(self, description: str, due_date: str):
        self.description = description
        self.due_date = due_date

    def save(self, username: str):
        with open(f'tasks_{username}.txt', 'a') as f:
            f.write(f"{self.description}|{self.due_date}\n")

    def remove(self, username: str):
        tasks = self.load(username)
        with open(f'tasks_{username}.txt', 'w') as f:
            for task in tasks:
                if task.description != self.description:
                    f.write(f"{task.description}|{task.due_date}\n")

    @staticmethod
    def load(username: str):
        tasks = []
        if os.path.exists(f'tasks_{username}.txt'):
            with open(f'tasks_{username}.txt', 'r') as f:
                for line in f:
                    task_data = line.strip().split('|')
                    tasks.append(Task(task_data[0], task_data[1]))
        return tasks

class App:
    def __init__(self):
        self.users = []
        self.tasks = {}

    def register(self, username: str, password: str, email: str) -> bool:
        if User.load(username) is None:
            user = User(username, password, email)
            user.save()
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        user = User.load(username)
        if user and user.password == password:
            session['username'] = username
            return True
        return False

    def add_task(self, username: str, description: str, due_date: str):
        task = Task(description, due_date)
        task.save(username)

    def remove_task(self, username: str, task_description: str):
        task = Task(task_description, "")
        task.remove(username)

    def get_tasks(self, username: str):
        return Task.load(username)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if App().login(username, password):
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if App().register(username, password, email):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'add_task' in request.form:
            description = request.form['description']
            due_date = request.form['due_date']
            App().add_task(username, description, due_date)
        elif 'remove_task' in request.form:
            task_description = request.form['task_description']
            App().remove_task(username, task_description)

    tasks = App().get_tasks(username)
    return render_template('home.html', tasks=tasks)

if __name__ == '__main__':
    app.run(port=8497, debug=False)
