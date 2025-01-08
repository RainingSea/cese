from flask import Flask, render_template, request, redirect, session
from UserManager import UserManager
from JournalManager import JournalManager
from JournalEntry import JournalEntry

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
journal_manager = JournalManager('journal_entries.txt')

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
        else:
            return "User already exists!"
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        entries = journal_manager.get_all_entries()
        return render_template('dashboard.html', entries=entries)
    return redirect('/')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return "Invalid credentials!"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = request.form['date']
        journal_manager.add_entry(JournalEntry(title, content, date))
        return redirect('/dashboard')
    return render_template('new_entry.html')

if __name__ == '__main__':
    app.run(port=8292, debug=False)
