from flask import Flask, render_template, request, redirect, url_for, session
from file_handler import FileHandler
from user_manager import UserManager
from task_manager import TaskManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

file_handler = FileHandler()
user_manager = UserManager(file_handler)
task_manager = TaskManager(file_handler)

def check_session():
    """Check if the user is logged in."""
    if 'username' not in session:
        return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.authenticate_user(username, password):
            session['username'] = username
            task_manager.load_tasks(username)  # Load tasks for the logged-in user
            return redirect(url_for('home'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register_user(username, password, email):
            return redirect(url_for('login'))
        else:
            return "Registration failed. Username may already exist."
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    """Display the home page with tasks."""
    check_session()  # Ensure the user is logged in

    username = session['username']
    if request.method == 'POST':
        task_description = request.form['task_description']
        due_date = request.form['due_date']
        task_manager.add_task(username, task_description, due_date)

    tasks = task_manager.get_tasks(username)
    return render_template('home.html', tasks=tasks)

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/remove_task/<int:task_id>', methods=['POST'])
def remove_task(task_id):
    """Remove a task by its ID for the logged-in user."""
    check_session()  # Ensure the user is logged in
    username = session['username']
    task_manager.remove_task(username, task_id)
    return redirect(url_for('home'))

if __name__ == '__main__':
    user_manager.load_users()
    app.run(port=8991, debug=False)
