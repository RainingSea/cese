from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from journal_manager import JournalManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

user_manager = UserManager()
journal_manager = JournalManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    entries = journal_manager.load_entries()
    return render_template('dashboard.html', entries=entries)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return redirect('/')

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        journal_manager.create_entry(title, content)
        return redirect('/dashboard')
    return render_template('new_entry.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8161, debug=False)
