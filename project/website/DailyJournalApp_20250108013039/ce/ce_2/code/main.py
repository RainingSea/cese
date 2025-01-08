from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from JournalManager import JournalManager
from JournalEntry import JournalEntry
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
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
        user_manager.register(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    entries = journal_manager.get_all_entries()
    return render_template('dashboard.html', entries=entries)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = JournalEntry(title, content, date)
        journal_manager.add_entry(entry)
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8290, debug=False)
