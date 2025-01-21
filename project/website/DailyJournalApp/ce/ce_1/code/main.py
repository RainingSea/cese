from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from journal_entry import JournalEntry

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and journal entries from files
def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_entries():
    entries = []
    with open('journal_entries.txt', 'r') as file:
        for line in file:
            title, content, date = line.strip().split('|')
            entries.append(JournalEntry(title, content, date))
    return entries

users = load_users()
entries = load_entries()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        users.append(new_user)
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', entries=entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_journal_entry = JournalEntry(title, content)
        entries.append(new_journal_entry)
        with open('journal_entries.txt', 'a') as file:
            file.write(f"{title}|{content}|{new_journal_entry.date}\n")
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html')

if __name__ == '__main__':
    app.run(port=8933, debug=False)
