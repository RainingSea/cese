from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

class FileStorage:
    def __init__(self):
        self.users_file = 'users.txt'
        self.tasks_file = 'tasks.txt'
        
        # Initialize files if they don't exist
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()
        if not os.path.exists(self.tasks_file):
            open(self.tasks_file, 'w').close()
    
    def read_users(self):
        users = {}
        with open(self.users_file, 'r') as f:
            for line in f:
                username, password, email = line.strip().split('|')
                users[username] = {'password': password, 'email': email}
        return users
    
    def write_user(self, username, password, email):
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}|{email}\n")
        return True
    
    def read_tasks(self):
        tasks = []
        with open(self.tasks_file, 'r') as f:
            for line in f:
                username, description, due_date, task_id = line.strip().split('|')
                tasks.append({
                    'username': username,
                    'description': description,
                    'due_date': due_date,
                    'task_id': task_id
                })
        return tasks
    
    def write_task(self, username, description, due_date):
        tasks = self.read_tasks()
        task_id = str(len(tasks) + 1)
        with open(self.tasks_file, 'a') as f:
            f.write(f"{username}|{description}|{due_date}|{task_id}\n")
        return True
    
    def delete_task(self, task_id):
        tasks = self.read_tasks()
        updated_tasks = [task for task in tasks if task['task_id'] != task_id]
        
        with open(self.tasks_file, 'w') as f:
            for task in updated_tasks:
                f.write(f"{task['username']}|{task['description']}|{task['due_date']}|{task['task_id']}\n")
        return True

class TaskManager:
    def __init__(self):
        self.storage = FileStorage()
    
    def login(self, username, password):
        users = self.storage.read_users()
        return username in users and users[username]['password'] == password
    
    def register(self, username, password, email):
        users = self.storage.read_users()
        if username in users:
            return False
        return self.storage.write_user(username, password, email)
    
    def add_task(self, username, description, due_date):
        return self.storage.write_task(username, description, due_date)
    
    def remove_task(self, task_id):
        return self.storage.delete_task(task_id)
    
    def get_tasks(self, username):
        tasks = self.storage.read_tasks()
        return [task for task in tasks if task['username'] == username]

task_manager = TaskManager()

@app.route('/')
def login_route():
    if 'username' in session:
        return redirect(url_for('home_route'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if task_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('home_route'))
    return render_template('login.html', error='Invalid credentials')

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if task_manager.register(username, password, email):
            return redirect(url_for('login_route'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home_route():
    if 'username' not in session:
        return redirect(url_for('login_route'))
    
    username = session['username']
    
    if request.method == 'POST':
        if 'description' in request.form:  # Adding task
            description = request.form['description']
            due_date = request.form['due_date']
            task_manager.add_task(username, description, due_date)
        elif 'task_id' in request.form:  # Removing task
            task_id = request.form['task_id']
            task_manager.remove_task(task_id)
    
    tasks = task_manager.get_tasks(username)
    return render_template('home.html', username=username, tasks=tasks)

@app.route('/logout')
def logout_route():
    session.pop('username', None)
    return redirect(url_for('login_route'))

if __name__ == '__main__':
    app.run(port=8118, debug=False)
