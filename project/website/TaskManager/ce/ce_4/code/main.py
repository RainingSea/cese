from flask import Flask, render_template, request, redirect, url_for, session
from TaskManager import TaskManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        manager = TaskManager(username, password)
        if manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Login Failed"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        manager = TaskManager(username, password, email)
        if manager.register(username, password, email):
            return redirect(url_for('login'))
        else:
            return "Registration Failed"
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    manager = TaskManager(username, '', '')
    
    if request.method == 'POST':
        task_description = request.form['task_description']
        due_date = request.form['due_date']
        manager.add_task(task_description, due_date)

    tasks = manager.get_tasks()
    return render_template('home.html', tasks=tasks)

if __name__ == '__main__':
    app.run(port=8990, debug=False)
