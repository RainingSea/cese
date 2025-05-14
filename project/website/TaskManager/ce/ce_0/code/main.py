from flask import Flask, render_template, request, redirect, url_for, session, json
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

class AuthManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file
        
    def validate_login(self, username, password):
        if not os.path.exists(self.users_file):
            return False
            
        with open(self.users_file, 'r') as f:
            for line in f:
                try:
                    user = json.loads(line)
                    if user['username'] == username and user['password'] == password:
                        return True
                except json.JSONDecodeError:
                    continue
        return False
        
    def register_user(self, username, password, email):
        if not username or not password or not email:
            return False
            
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                for line in f:
                    try:
                        user = json.loads(line)
                        if user['username'] == username:
                            return False
                    except json.JSONDecodeError:
                        continue
                        
        new_user = {'username': username, 'password': password, 'email': email}
        with open(self.users_file, 'a') as f:
            f.write(json.dumps(new_user) + '\n')
        return True

class TaskManager:
    def __init__(self, tasks_file='tasks.txt'):
        self.tasks_file = tasks_file
        
    def get_tasks(self, username):
        tasks = []
        if not os.path.exists(self.tasks_file):
            return tasks
            
        with open(self.tasks_file, 'r') as f:
            for line in f:
                try:
                    task = json.loads(line)
                    if task['username'] == username:
                        tasks.append(task)
                except json.JSONDecodeError:
                    continue
        return tasks
        
    def add_task(self, username, description, due_date):
        if not username or not description or not due_date:
            return False
            
        new_task = {'username': username, 'description': description, 'due_date': due_date}
        with open(self.tasks_file, 'a') as f:
            f.write(json.dumps(new_task) + '\n')
        return True
        
    def remove_task(self, username, task_index):
        tasks = []
        removed = False
        
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as f:
                for line in f:
                    try:
                        task = json.loads(line)
                        if task['username'] == username:
                            if task_index == 0:
                                removed = True
                            else:
                                tasks.append(line)
                            task_index -= 1
                        else:
                            tasks.append(line)
                    except json.JSONDecodeError:
                        continue
                        
        if removed:
            with open(self.tasks_file, 'w') as f:
                f.writelines(tasks)
            return True
        return False

auth_manager = AuthManager()
task_manager = TaskManager()

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    tasks = task_manager.get_tasks(session['username'])
    return render_template('home.html', username=session['username'], tasks=tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_manager.validate_login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if auth_manager.register_user(username, password, email):
            return redirect(url_for('login'))
        return render_template('register.html', error='Registration failed')
    return render_template('register.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'username' not in session:
        return redirect(url_for('login'))
    description = request.form['description']
    due_date = request.form['due_date']
    task_manager.add_task(session['username'], description, due_date)
    return redirect(url_for('home'))

@app.route('/remove_task/<int:task_index>')
def remove_task(task_index):
    if 'username' not in session:
        return redirect(url_for('login'))
    task_manager.remove_task(session['username'], task_index)
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8117, debug=False)
