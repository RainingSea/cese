from flask import Flask, render_template, request, redirect, url_for, session
import os
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key'

class TaskManager:
    def __init__(self):
        self.users_file = 'users.txt'
        self.tasks_file = 'tasks.txt'
        self.init_files()

    def init_files(self):
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()
        if not os.path.exists(self.tasks_file):
            open(self.tasks_file, 'w').close()

    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) >= 2 and parts[0] == username and parts[1] == password:
                    return True
        return False

    def register(self, username, password, email):
        if not username or not password or not email:
            return False
        
        with open(self.users_file, 'r') as f:
            for line in f:
                if line.startswith(username + ':'):
                    return False

        with open(self.users_file, 'a') as f:
            f.write(f"{username}:{password}:{email}\n")
        return True

    def add_task(self, username, description, due_date):
        if not username or not description or not due_date:
            return False
        
        task_id = 1
        with open(self.tasks_file, 'r') as f:
            for line in f:
                if line.strip():
                    task_id += 1

        with open(self.tasks_file, 'a') as f:
            f.write(f"{username}:{description}:{due_date}:{task_id}\n")
        return True

    def remove_task(self, username, task_id):
        lines = []
        removed = False
        
        with open(self.tasks_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) >= 4 and parts[0] == username and parts[3] == task_id:
                    removed = True
                else:
                    lines.append(line)

        if removed:
            with open(self.tasks_file, 'w') as f:
                f.writelines(lines)
        return removed

    def get_tasks(self, username):
        tasks = []
        with open(self.tasks_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) >= 4 and parts[0] == username:
                    tasks.append({
                        'description': parts[1],
                        'due_date': parts[2],
                        'id': parts[3]
                    })
        return tasks

task_manager = TaskManager()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if task_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if task_manager.register(username, password, email):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error='Registration failed')
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    if request.method == 'POST':
        if 'description' in request.form:
            description = request.form['description']
            due_date = request.form['due_date']
            task_manager.add_task(username, description, due_date)
        elif 'task_id' in request.form:
            task_id = request.form['task_id']
            task_manager.remove_task(username, task_id)
    
    tasks = task_manager.get_tasks(username)
    return render_template('home.html', username=username, tasks=tasks)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8119, debug=False)
