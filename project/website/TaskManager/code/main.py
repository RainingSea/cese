from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from user_manager import UserManager
from task_manager import TaskManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

user_manager = UserManager('users.txt')
task_manager = TaskManager('tasks.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/home')
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            flash('Registration successful! Please log in.')
            return redirect('/')
        else:
            flash('Registration failed. Username may already exist.')
    return render_template('registration.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect('/')
    
    username = session['username']
    if request.method == 'POST':
        if 'add_task' in request.form:
            description = request.form['description']
            due_date = request.form['due_date']
            task_manager.add_task(username, description, due_date)
        elif 'remove_task' in request.form:
            task_id = int(request.form['task_id'])
            task_manager.remove_task(username, task_id)

    tasks = task_manager.get_tasks(username)
    return render_template('home.html', tasks=tasks)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8257, debug=False)
