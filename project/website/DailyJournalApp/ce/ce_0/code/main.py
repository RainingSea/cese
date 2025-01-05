from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def validate(username: str, password: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

class JournalEntry:
    def __init__(self, title: str, content: str, date: str):
        self.title = title
        self.content = content
        self.date = date

    def save(self):
        with open('journal_entries.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.date}\n")

class JournalApp:
    def __init__(self):
        self.users = []
        self.entries = []

    def register(self, username: str, password: str) -> bool:
        if not User.validate(username, password):
            user = User(username, password)
            user.save()
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        if User.validate(username, password):
            session['username'] = username
            return True
        return False

    def create_entry(self, title: str, content: str) -> None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = JournalEntry(title, content, date)
        entry.save()

    def get_entries(self) -> list:
        entries = []
        with open('journal_entries.txt', 'r') as f:
            for line in f:
                title, content, date = line.strip().split('|')
                entries.append({'title': title, 'content': content, 'date': date})
        return entries

app = Flask(__name__)
app.secret_key = 'your_secret_key'
journal_app = JournalApp()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if journal_app.login(username, password):
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
    app.run(port=8085, debug=False)
