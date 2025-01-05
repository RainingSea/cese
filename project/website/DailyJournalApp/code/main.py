from flask import Flask, render_template, request, redirect, session
from user import User
from journal_entry import JournalEntry
from session_manager import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

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
            title, content, date = line.strip().split('|')
            entries.append(JournalEntry(title, content, date))
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
        with open('users.txt', 'a') as file:
            file.write(f"{user.username}|{user.password}\n")
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    entries = load_journal_entries()
    return render_template('dashboard.html', entries=entries)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect('/dashboard')
    return redirect('/')

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = request.form['date']
        entry = JournalEntry(title, content, date)
        with open('journal_entries.txt', 'a') as file:
            file.write(f"{entry.title}|{entry.content}|{entry.date}\n")
        return redirect('/dashboard')
    return render_template('new_entry.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8019, debug=False)
