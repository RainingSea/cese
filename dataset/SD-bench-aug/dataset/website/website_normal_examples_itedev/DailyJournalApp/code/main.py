from flask import Flask, render_template, request, redirect, session, url_for
from user import User
from journal_entry import JournalEntry
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Load users from the users.txt file
def load_users():
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    except FileNotFoundError:
        pass
    return users

# Save a new user to the users.txt file
def save_user(user):
    with open('users.txt', 'a') as file:
        file.write(f"{user.username}|{user.password}\n")

# Load journal entries from the journal_entries.txt file
def load_entries():
    entries = []
    try:
        with open('journal_entries.txt', 'r') as file:
            for line in file:
                title, content, date = line.strip().split('|')
                entries.append(JournalEntry(title, content, date))
    except FileNotFoundError:
        pass
    return entries

# Save a new journal entry to the journal_entries.txt file
def save_entry(entry):
    with open('journal_entries.txt', 'a') as file:
        file.write(f"{entry.title}|{entry.content}|{entry.date}\n")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
        return "Invalid credentials, please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        save_user(new_user)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    entries = load_entries()
    return render_template('dashboard.html', username=session['username'], entries=entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = JournalEntry(title, content, date)
        save_entry(new_entry)
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)