from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from journal_entry import JournalEntry

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class App:
    def __init__(self):
        self.users = self.load_users()
        self.entries = self.load_entries()

    def load_users(self):
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
        return users

    def load_entries(self):
        entries = []
        with open('journal_entries.txt', 'r') as file:
            for line in file:
                title, content, date = line.strip().split('|')
                entries.append(JournalEntry(title, content, date))
        return entries

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                session['username'] = username
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        return True

    def create_entry(self, title: str, content: str) -> None:
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = JournalEntry(title, content, date)
        new_entry.save_entry()
        self.entries.append(new_entry)

    def get_entries(self):
        return self.entries

app_instance = App()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if app_instance.login(username, password):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_page'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if app_instance.register(username, password):
        return redirect(url_for('login_page'))
    return redirect(url_for('login_page'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        entries = app_instance.get_entries()
        return render_template('dashboard.html', entries=entries)
    return redirect(url_for('login_page'))

@app.route('/new_entry', methods=['POST'])
def new_entry():
    if 'username' in session:
        title = request.form['title']
        content = request.form['content']
        app_instance.create_entry(title, content)
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(port=8362, debug=False)
