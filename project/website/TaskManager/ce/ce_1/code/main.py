from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
                    self.users[username] = {'password': password, 'email': email}

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = {'password': password, 'email': email}
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username]['password'] == password:
            session['username'] = username
            return True
        return False

class TaskManager:
    def __init__(self, username):
        self.filename = f'tasks_{username}.txt'
        self.load_tasks()

    def load_tasks(self):
        self.tasks = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    task_id, description, due_date = line.strip().split('|')
                    self.tasks.append({'id': int(task_id), 'description': description, 'due_date': due_date})

    def add_task(self, description: str, due_date: str) -> bool:
        task_id = len(self.tasks) + 1
        self.tasks.append({'id': task_id, 'description': description, 'due_date': due_date})
        with open(self.filename, 'a') as file:
            file.write(f"{task_id}|{description}|{due_date}\n")
        return True

    def remove_task(self, task_id: int) -> bool:
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self.save_tasks()
        return True

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            for task in self.tasks:
                file.write(f"{task['id']}|{task['description']}|{task['due_date']}\n")

    def get_tasks(self):
        return self.tasks

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user_manager = UserManager('users.txt')
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
        else:
            return "Username already exists!", 400
    return render_template('registration.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    task_manager = TaskManager(username)

    if request.method == 'POST':
        if 'add_task' in request.form:
            description = request.form['description']
            due_date = request.form['due_date']
            task_manager.add_task(description, due_date)
        elif 'remove_task' in request.form:
            task_id = int(request.form['remove_task'])
            task_manager.remove_task(task_id)

    tasks = task_manager.get_tasks()
    return render_template('home.html', tasks=tasks)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8427, debug=False)
