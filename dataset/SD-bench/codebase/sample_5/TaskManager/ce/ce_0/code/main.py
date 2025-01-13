from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from task import Task

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.authenticate():
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    task_manager = Task()
    
    if request.method == 'POST':
        if 'add_task' in request.form:
            description = request.form['description']
            due_date = request.form['due_date']
            task_manager = Task(description, due_date)
            task_manager.save(username)
        elif 'remove_task' in request.form:
            task_index = int(request.form['task_index'])
            task_manager.remove_task(username, task_index)

    tasks = task_manager.load_tasks(username)
    return render_template('home.html', tasks=tasks)

if __name__ == '__main__':
    app.run(port=8494, debug=False)
