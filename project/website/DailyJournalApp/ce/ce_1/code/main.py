from flask import Flask, render_template, request, redirect, session, url_for
from user import User
from journal_entry import JournalEntry
from session_manager import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production

def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password, entries = line.strip().split('|')
            users[username] = User(username, password)
    return users

def load_journal_entries():
    entries = []
    with open('journal_entries.txt', 'r') as file:
        for line in file:
            title, content, date = line.strip().split('|')
            entries.append(JournalEntry(title, content, date))
    return entries

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    entries = load_journal_entries()
    return render_template('dashboard.html', entries=entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_journal_entry = JournalEntry(title, content)
        new_journal_entry.save()
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8018, debug=False)
