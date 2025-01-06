from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from journal_manager import JournalManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

user_manager = UserManager()
journal_manager = JournalManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
        else:
            return "User already exists", 400
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    entries = journal_manager.load_entries()
    return render_template('dashboard.html', entries=entries)

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
    app.run(port=8160, debug=False)
