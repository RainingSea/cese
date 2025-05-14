from flask import Flask, render_template, request, redirect, url_for, session
import os
import uuid
import datetime
from threading import Lock

app = Flask(__name__)
app.secret_key = 'secret_key'

class TaskManager:
    def __init__(self):
        self.users_file = 'users.txt'
        self.tasks_file = 'tasks.txt'
        self.lock = Lock()
        self._initialize_files()

    def _initialize_files(self):
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                f.write("admin|admin123|admin@example.com\n")
        if not os.path.exists(self.tasks_file):
            open(self.tasks_file, 'w').close()

    def validate_login(self, username, password):
        with self.lock, open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 2 and parts[0] == username and parts[1] == password:
                    return True
        return False

    def register_user(self, username, password, email):
        if not username or not password or not email:
            return False

        with self.lock, open(self.users_file, 'r+') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == username:
                    return False
            
            f.write(f"{username}|{password}|{email}\n")
            return True

    def add_task(self, username, description, due_date):
        try:
            due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        except ValueError:
            return None

        task_id = str(uuid.uuid4())
        with self.lock, open(self.tasks_file, 'a') as f:
            f.write(f"{username}|{description}|{due_date}|{task_id}\n")
        return task_id

    def delete_task(self, username, task_id):
        lines = []
        found = False
        
        with self.lock, open(self.tasks_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4 and parts[3] == task_id and parts[0] == username:
                    found = True
                else:
                    lines.append(line)
        
        if found:
            with self.lock, open(self.tasks_file, 'w') as f:
                f.writelines(lines)
            return True
        return False

    def get_user_tasks(self, username):
        tasks = []
        with self.lock, open(self.tasks_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4 and parts[0] == username:
                    tasks.append({
                        'description': parts[1],
                        'due_date': parts[2],
                        'task_id': parts[3]
                    })
        return tasks

task_manager = TaskManager()

@app.route('/', methods=['GET', 'POST'])
def handle_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if task_manager.validate_login(username, password):
            session['username'] = username
            return redirect(url_for('handle_home'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def handle_registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if len(username) < 4 or ' ' in username:
            return render_template('register.html', error="Username must be at least 4 characters with no spaces")
        if len(password) < 6:
            return render_template('register.html', error="Password must be at least 6 characters")
        if '@' not in email:
            return render_template('register.html', error="Invalid email format")
            
        if task_manager.register_user(username, password, email):
            return redirect(url_for('handle_login'))
        else:
            return render_template('register.html', error="Username already exists")
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def handle_home():
    if 'username' not in session:
        return redirect(url_for('handle_login'))
    
    username = session['username']
    
    if request.method == 'POST':
        if 'description' in request.form:
            description = request.form['description']
            due_date = request.form['due_date']
            task_id = task_manager.add_task(username, description, due_date)
            if not task_id:
                return render_template('home.html', 
                                    username=username,
                                    tasks=task_manager.get_user_tasks(username),
                                    error="Invalid date format (use YYYY-MM-DD)")
        elif 'task_id' in request.form:
            task_id = request.form['task_id']
            if not task_manager.delete_task(username, task_id):
                return render_template('home.html', 
                                    username=username,
                                    tasks=task_manager.get_user_tasks(username),
                                    error="Failed to delete task")
    
    return render_template('home.html', 
                         username=username,
                         tasks=task_manager.get_user_tasks(username))

@app.route('/logout')
def handle_logout():
    session.pop('username', None)
    return redirect(url_for('handle_login'))

if __name__ == '__main__':
    app.run(port=8124, debug=False)
