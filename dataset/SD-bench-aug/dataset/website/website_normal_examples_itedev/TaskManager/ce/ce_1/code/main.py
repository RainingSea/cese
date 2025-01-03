from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from task_manager import TaskManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize UserManager and TaskManager
user_manager = UserManager('users.txt')
task_manager = TaskManager('tasks_template.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'add_task' in request.form:
            task_description = request.form['task_description']
            due_date = request.form['due_date']
            task_manager.add_task(task_description, due_date, session['username'])
        elif 'remove_task' in request.form:
            task_description = request.form['task_description']
            task_manager.remove_task(task_description, session['username'])

    tasks = task_manager.get_tasks(session['username'])
    return render_template('home.html', tasks=tasks)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)