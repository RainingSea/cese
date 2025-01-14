from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from TaskManager import TaskManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
task_manager = TaskManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
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
    
    username = session['username']
    if request.method == 'POST':
        task_description = request.form['task_description']
        due_date = request.form['due_date']
        task_manager.add_task(username, task_description, due_date)

    tasks = task_manager.load_tasks(username)
    return render_template('home.html', tasks=tasks)

@app.route('/remove_task', methods=['POST'])
def remove_task():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    task_description = request.form['task_description']
    task_manager.remove_task(username, task_description)

    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8464, debug=False)
