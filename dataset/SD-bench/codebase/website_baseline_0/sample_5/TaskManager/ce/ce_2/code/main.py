from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username},{self.password},{self.email}\n")

    @staticmethod
    def load(username: str) -> 'User':
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split(',')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1], user_data[2])
        return None

class Task:
    def __init__(self, description: str, due_date: str):
        self.description = description
        self.due_date = due_date

    def save(self, username: str) -> None:
        with open(f'tasks_{username}.txt', 'a') as f:
            f.write(f"{self.description},{self.due_date}\n")

    @staticmethod
    def load(username: str) -> list:
        tasks = []
        if os.path.exists(f'tasks_{username}.txt'):
            with open(f'tasks_{username}.txt', 'r') as f:
                for line in f:
                    task_data = line.strip().split(',')
                    tasks.append(Task(task_data[0], task_data[1]))
        return tasks

    @staticmethod
    def remove(username: str, task_index: int) -> None:
        tasks = Task.load(username)
        if 0 <= task_index < len(tasks):
            del tasks[task_index]
            with open(f'tasks_{username}.txt', 'w') as f:
                for task in tasks:
                    f.write(f"{task.description},{task.due_date}\n")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.load(username)
        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    tasks = Task.load(username)

    if request.method == 'POST':
        task_description = request.form['task_description']
        due_date = request.form['due_date']
        new_task = Task(task_description, due_date)
        new_task.save(username)
        return redirect(url_for('home'))

    return render_template('home.html', tasks=tasks)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8496, debug=False)
