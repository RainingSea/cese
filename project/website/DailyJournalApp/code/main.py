from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self, username: str, password: str) -> bool:
        if not self.username_exists(username):
            with open('users.txt', 'a') as f:
                f.write(f"{username}|{password}\n")
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

    def username_exists(self, username: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                stored_username, _ = line.strip().split('|')
                if stored_username == username:
                    return True
        return False

class JournalEntry:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save_entry(self) -> bool:
        with open('journal_entries.txt', 'a') as f:
            f.write(f"{session['username']}|{self.title}|{self.content}|{self.date}\n")
        return True

    @staticmethod
    def get_entries() -> list:
        entries = []
        with open('journal_entries.txt', 'r') as f:
            for line in f:
                entries.append(line.strip().split('|'))
        return entries

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Username already exists!"
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.login(username, password):
            session['username'] = username
            return render_template('dashboard.html', username=username, entries=JournalEntry.get_entries())
        else:
            return "Invalid credentials!"
    return render_template('dashboard.html', username=session.get('username'), entries=JournalEntry.get_entries())

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        entry = JournalEntry(title, content)
        entry.save_entry()
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)