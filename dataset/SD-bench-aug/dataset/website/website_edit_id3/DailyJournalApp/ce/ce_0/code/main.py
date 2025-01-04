from flask import Flask, render_template, request, redirect, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key for production

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load_users() -> list:
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

class JournalEntry:
    def __init__(self, title: str, content: str, date: str):
        self.title = title
        self.content = content
        self.date = date

    def save_entry(self):
        with open('journal_entries.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.date}\n")

    @staticmethod
    def load_entries() -> list:
        entries = []
        try:
            with open('journal_entries.txt', 'r') as f:
                for line in f:
                    title, content, date = line.strip().split('|')
                    entries.append(JournalEntry(title, content, date))
        except FileNotFoundError:
            pass
        return entries

class Auth:
    @staticmethod
    def login(username: str, password: str) -> bool:
        users = User.load_users()
        for user in users:
            if user.username == username and user.password == password:
                return True
        return False

    @staticmethod
    def register(username: str, password: str) -> bool:
        users = User.load_users()
        if any(user.username == username for user in users):
            return False
        new_user = User(username, password)
        new_user.save()
        return True

    @staticmethod
    def logout():
        session.pop('username', None)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Auth.register(username, password):
            return redirect('/')
        else:
            return "Username already exists!"
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    entries = JournalEntry.load_entries()
    return render_template('dashboard.html', entries=entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = JournalEntry(title, content, date)
        entry.save_entry()
        return redirect('/dashboard')
    return render_template('new_entry.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if Auth.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return "Invalid credentials!"

@app.route('/logout')
def logout():
    Auth.logout()
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8125, debug=True)
