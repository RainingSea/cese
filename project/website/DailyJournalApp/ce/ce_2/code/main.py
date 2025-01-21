from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from journal_entry import JournalEntry
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class JournalApp:
    def __init__(self):
        self.users = self.load_users()
        self.entries = self.load_entries()

    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def load_entries(self):
        entries = []
        if os.path.exists('journal_entries.txt'):
            with open('journal_entries.txt', 'r') as file:
                for line in file:
                    title, content, date = line.strip().split('|')
                    entries.append(JournalEntry(title, content, date))
        return entries

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.validate_password(password):
                return True
        return False

    def create_entry(self, title: str, content: str) -> None:
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = JournalEntry(title, content, date)
        new_entry.save()
        self.entries.append(new_entry)

    def get_entries(self):
        return self.entries

journal_app = JournalApp()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if journal_app.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if journal_app.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    entries = journal_app.get_entries()
    return render_template('dashboard.html', entries=entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        journal_app.create_entry(title, content)
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8934, debug=False)
