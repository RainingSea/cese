from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from journal_entry import JournalEntry
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_journal_entries():
    entries = []
    with open('journal_entries.txt', 'r') as file:
        for line in file:
            title, date, content = line.strip().split('|')
            entries.append(JournalEntry(title, date, content))
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
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = JournalEntry(title, date, content)
        entry.save()
    entries = load_journal_entries()
    return render_template('dashboard.html', entries=entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    return render_template('new_entry.html')

if __name__ == '__main__':
    app.run(port=8527, debug=False)
