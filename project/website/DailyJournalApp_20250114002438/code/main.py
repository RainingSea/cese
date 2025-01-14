from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from journal_entry import JournalEntry
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
users = []
entries = []

def load_users():
    """Load users from the users.txt file."""
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))

def load_entries():
    """Load journal entries from the journal_entries.txt file."""
    if os.path.exists('journal_entries.txt'):
        with open('journal_entries.txt', 'r') as file:
            for line in file:
                title, content, date = line.strip().split('|')
                entries.append(JournalEntry(title, content, date))

@app.route('/')
def login():
    """Render the login page."""
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    """Handle user login."""
    username = request.form['username']
    password = request.form['password']
    for user in users:
        if user.validate(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.save():
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Render the dashboard page with journal entries."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', entries=entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    """Handle creating a new journal entry."""
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        entry = JournalEntry(title, content, '2023-10-01')  # Example date
        entry.save()
        entries.append(entry)
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html')

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    load_users()
    load_entries()
    app.run(port=8455, debug=False)
