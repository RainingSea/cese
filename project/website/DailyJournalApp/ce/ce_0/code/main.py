from flask import Flask, render_template, request, redirect, url_for, session
from typing import List
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load(username: str):
        with open('users.txt', 'r') as f:
            for line in f:
                user_info = line.strip().split('|')
                if user_info[0] == username:
                    return User(user_info[0], user_info[1])
        return None

class JournalEntry:
    def __init__(self, title: str, content: str, date: str):
        self.title = title
        self.content = content
        self.date = date

    def save(self):
        with open('journal_entries.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.date}\n")

    @staticmethod
    def load_all() -> List['JournalEntry']:
        entries = []
        with open('journal_entries.txt', 'r') as f:
            for line in f:
                entry_info = line.strip().split('|')
                if len(entry_info) == 3:
                    entries.append(JournalEntry(entry_info[0], entry_info[1], entry_info[2]))
        return entries

class Session:
    def __init__(self, username: str):
        self.username = username

    def save(self):
        with open('sessions.txt', 'a') as f:
            f.write(f"{self.username}\n")

    @staticmethod
    def load() -> str:
        if os.path.exists('sessions.txt'):
            with open('sessions.txt', 'r') as f:
                session_data = f.readline().strip()
                return session_data
        return ''

@app.route('/')
def login():
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
    entries = JournalEntry.load_all()
    return render_template('dashboard.html', entries=entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = request.form['date']
        new_entry = JournalEntry(title, content, date)
        new_entry.save()
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def do_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.load(username)
        if user and user.password == password:
            session['username'] = user.username
            new_session = Session(username)
            new_session.save()
            return redirect(url_for('dashboard'))
    return render_template('login.html', error='Invalid credentials.')

if __name__ == '__main__':
    app.run(port=8017, debug=False)
