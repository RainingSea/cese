from flask import Flask, render_template, request, redirect, session
from task_manager import TaskManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
task_manager = TaskManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if task_manager.authenticate_user(username, password):
            session['username'] = username
            return redirect('/home')
        return redirect('/')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        task_manager.register_user(username, password, email)
        return redirect('/')
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    if request.method == 'POST':
        task_description = request.form['task_description']
        due_date = request.form['due_date']
        task_manager.add_task(username, task_description, due_date)
    tasks = task_manager.load_tasks(username)
    return render_template('home.html', tasks=tasks)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8197, debug=False)
