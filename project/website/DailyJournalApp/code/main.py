from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from user import User
from journal_entry import JournalEntry

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production

class App:
    def __init__(self):
        self.users = User.load_users()
        self.entries = JournalEntry.load_entries()

    def run(self):
        app.run(port=8363, debug=False)

    def register_user(self, username: str, password: str) -> None:
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)

    def login_user(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                session['username'] = username
                return True
        return False

    def create_entry(self, title: str, content: str) -> None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = JournalEntry(title, content, date)
        new_entry.save()
        self.entries.append(new_entry)

    def get_entries(self) -> list:
        return self.entries

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app_instance.register_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    entries = app_instance.get_entries()
    return render_template('dashboard.html', entries=entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        app_instance.create_entry(title, content)
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app_instance = App()
    app_instance.run()