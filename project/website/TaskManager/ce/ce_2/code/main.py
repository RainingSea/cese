from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from task_manager import TaskManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

user_manager = UserManager('users.txt')
task_manager = None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            global task_manager
            task_manager = TaskManager(f'tasks_{username}.txt')
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
    if request.method == 'POST':
        if 'add_task' in request.form:
            task_description = request.form['task_description']
            due_date = request.form['due_date']
            task_manager.add_task(task_description, due_date)
        elif 'remove_task' in request.form:
            task_index = int(request.form['task_index'])
            task_manager.remove_task(task_index)
    tasks = task_manager.get_tasks() if task_manager else []
    return render_template('home.html', tasks=tasks)

if __name__ == '__main__':
    app.run(port=8256, debug=False)
