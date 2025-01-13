from flask import Flask, render_template, request, redirect, session
from user import User
from journal_entry import JournalEntry
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
users = []
entries = []

def load_users():
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))

def load_entries():
    if os.path.exists('journal_entries.txt'):
        with open('journal_entries.txt', 'r') as file:
            for line in file:
                title, content, date = line.strip().split('|')
                entries.append(JournalEntry(title, content, date))

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        users.append(user)
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', entries=entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        entry = JournalEntry(title, content)
        entries.append(entry)
        with open('journal_entries.txt', 'a') as file:
            file.write(f"{title}|{content}|{entry.date}\n")
        return redirect('/dashboard')
    return render_template('new_entry.html')

if __name__ == '__main__':
    load_users()
    load_entries()
    app.run(port=8443, debug=False)
