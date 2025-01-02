from flask import Flask, render_template, request, redirect, session
from user import User
from task import Task

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        new_user.save()
        return redirect('/')
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect('/')
    
    username = session['username']
    
    if request.method == 'POST':
        if 'task_description' in request.form:
            task_description = request.form['task_description']
            due_date = request.form['due_date']
            new_task = Task(task_description, due_date)
            new_task.save(username)
        elif 'remove_task' in request.form:
            task_description = request.form['remove_task']
            Task.remove_task(username, task_description)
    
    tasks = Task.load_tasks(username)
    return render_template('home.html', tasks=tasks)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = User.load_users()
    
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect('/home')
    
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8153, debug=True)
