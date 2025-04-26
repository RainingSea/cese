from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as f:
            return [line.strip().split('|') for line in f.readlines()]

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append([username, password])
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

class JournalManager:
    def __init__(self):
        self.entries = self.load_entries()

    def load_entries(self):
        if not os.path.exists('entries.txt'):
            return []
        with open('entries.txt', 'r') as f:
            return [line.strip().split('|') for line in f.readlines()]

    def create_entry(self, title: str, content: str) -> None:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = [title, content, timestamp]
        self.entries.append(entry)
        with open('entries.txt', 'a') as f:
            f.write(f"{title}|{content}|{timestamp}\n")

    def get_entries(self):
        return self.entries

user_manager = UserManager()
journal_manager = JournalManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    entries = journal_manager.get_entries()
    return render_template('dashboard.html', entries=entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        journal_manager.create_entry(title, content)
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8156, debug=False)
