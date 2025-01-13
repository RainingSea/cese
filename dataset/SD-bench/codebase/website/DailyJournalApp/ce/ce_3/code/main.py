from flask import Flask, render_template, request, redirect, url_for, session
from User import User
from JournalEntry import JournalEntry

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

class App:
    def __init__(self):
        self.users = []
        self.entries = []
        self.load_users()
        self.load_entries()

    def load_users(self):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                self.users.append(User(username, password))

    def load_entries(self):
        with open('journal_entries.txt', 'r') as file:
            for line in file:
                title, date, content = line.strip().split(',')
                self.entries.append(JournalEntry(title, date, content))

    def register(self, username, password):
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        self.users.append(new_user)
        new_user.save()
        return True

    def login(self, username, password):
        return any(user.check_credentials(username, password) for user in self.users)

    def create_entry(self, title, content):
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = JournalEntry(title, date, content)
        self.entries.append(new_entry)
        new_entry.save()

    def get_entries(self):
        return self.entries

app_instance = App()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app_instance.register(username, password):
            return redirect(url_for('login'))
        return "Registration failed. Username may already exist."
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', entries=app_instance.get_entries())

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        app_instance.create_entry(title, content)
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html')

if __name__ == '__main__':
    app.run(port=8445, debug=False)
