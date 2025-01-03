from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from task_manager import TaskManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

user_manager = UserManager()
task_manager = TaskManager()

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
    
    username = session['username']
    
    if request.method == 'POST':
        if 'logout' in request.form:
            session.pop('username', None)
            return redirect(url_for('login'))
        elif 'add_task' in request.form:
            description = request.form['task_description']
            due_date = request.form['due_date']
            task_manager.add_task(username, description, due_date)
    
    tasks = task_manager.load_tasks(username)
    return render_template('home.html', tasks=tasks)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('home'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8143, debug=True)
