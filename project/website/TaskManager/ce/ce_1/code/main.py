from flask import Flask, request, redirect, render_template, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

class TaskManager:
    def __init__(self):
        self.users = self.load_users()
        
    def load_users(self):
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split(',')
                    users[username] = {'password': password, 'email': email}
        return users

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = {'password': password, 'email': email}
        with open('users.txt', 'a') as file:
            file.write(f"{username},{password},{email}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            return True
        return False

    def add_task(self, username: str, task_description: str, due_date: str) -> None:
        with open(f'tasks_{username}.txt', 'a') as file:
            file.write(f"{task_description},{due_date}\n")

    def remove_task(self, username: str, task_index: int) -> None:
        tasks = self.get_tasks(username)
        if 0 <= task_index < len(tasks):
            tasks.pop(task_index)
            with open(f'tasks_{username}.txt', 'w') as file:
                for task in tasks:
                    file.write(f"{task[0]},{task[1]}\n")

    def get_tasks(self, username: str) -> list:
        tasks = []
        if os.path.exists(f'tasks_{username}.txt'):
            with open(f'tasks_{username}.txt', 'r') as file:
                for line in file:
                    task_description, due_date = line.strip().split(',')
                    tasks.append((task_description, due_date))
        return tasks

task_manager = TaskManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if task_manager.login(username, password):
            return redirect('/home')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if task_manager.register(username, password, email):
            return redirect('/')
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect('/')
    
    username = session['username']
    if request.method == 'POST':
        if 'add_task' in request.form:
            task_description = request.form['task_description']
            due_date = request.form['due_date']
            task_manager.add_task(username, task_description, due_date)
        elif 'remove_task' in request.form:
            task_index = int(request.form['task_index'])
            task_manager.remove_task(username, task_index)

    tasks = task_manager.get_tasks(username)
    return render_template('home.html', tasks=tasks)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8255, debug=False)
