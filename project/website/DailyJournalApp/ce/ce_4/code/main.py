from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    def validate(self) -> bool:
        users = self.load_users()
        return any(user.username == self.username and user.password == self.password for user in users)

    @staticmethod
    def load_users():
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f.readlines():
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

class JournalEntry:
    def __init__(self, title: str, content: str, date: str):
        self.title = title
        self.content = content
        self.date = date

    def save(self):
        with open('entries.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.date}\n")

class JournalApp:
    def __init__(self):
        self.users = User.load_users()
        self.entries = self.load_entries()

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        user = User(username, password)
        return user.validate()

    def create_entry(self, title: str, content: str) -> None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = JournalEntry(title, content, date)
        entry.save()
        self.entries.append(entry)

    def get_entries(self) -> list:
        return self.entries

    @staticmethod
    def load_entries():
        entries = []
        if os.path.exists('entries.txt'):
            with open('entries.txt', 'r') as f:
                for line in f.readlines():
                    title, content, date = line.strip().split('|')
                    entries.append(JournalEntry(title, content, date))
        return entries

journal_app = JournalApp()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if journal_app.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Registration failed. Username already exists."
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        journal_app.create_entry(title, content)
        return redirect(url_for('dashboard'))
    entries = journal_app.get_entries()
    return render_template('dashboard.html', entries=entries)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if journal_app.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Login failed. Check your username and password."

if __name__ == '__main__':
    app.run(port=8528, debug=False)
