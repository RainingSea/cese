from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
                user_data = line.strip().split('|')
                if user_data[0] == username and user_data[1] == password:
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
        return User.validate(username, password)

    def create_entry(self, title: str, content: str) -> None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = JournalEntry(title, content, date)
        entry.save()

    def get_entries(self) -> list:
        entries = []
        with open('journal_entries.txt', 'r') as f:
            for line in f:
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
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        journal_app.create_entry(title, content)
    entries = journal_app.get_entries()
    return render_template('dashboard.html', entries=entries)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8087, debug=False)
