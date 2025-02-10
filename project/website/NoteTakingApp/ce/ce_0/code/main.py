from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Note:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def to_string(self) -> str:
        return f"{self.title}|{self.content}"

def load_users() -> dict:
    users = {}
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
    return users

def save_users(users: dict) -> None:
    with open('users.txt', 'w') as file:
        for username, password in users.items():
            file.write(f"{username}|{password}\n")

def load_notes(username: str) -> list:
    notes = []
    filename = f'notes_{username}.txt'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                notes.append(Note(title, content))
    return notes

def save_note(username: str, title: str, content: str) -> None:
    filename = f'notes_{username}.txt'
    with open(filename, 'a') as file:
        note = Note(title, content)
        file.write(note.to_string() + '\n')

def delete_note(username: str, title: str) -> None:
    filename = f'notes_{username}.txt'
    notes = load_notes(username)
    with open(filename, 'w') as file:
        for note in notes:
            if note.title != title:
                file.write(note.to_string() + '\n')

def search_notes(username: str, query: str) -> list:
    notes = load_notes(username)
    return [note for note in notes if query.lower() in note.title.lower() or query.lower() in note.content.lower()]

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username not in users:
            users[username] = password
            save_users(users)
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        notes = load_notes(session['username'])
        return render_template('dashboard.html', notes=notes)
    return redirect(url_for('login'))

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        save_note(session['username'], title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>')
def view_note(title):
    if 'username' in session:
        notes = load_notes(session['username'])
        note = next((note for note in notes if note.title == title), None)
        return render_template('view_note.html', note=note)
    return redirect(url_for('login'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if request.method == 'POST':
        query = request.form['query']
        results = search_notes(session['username'], query)
        return render_template('search_note.html', results=results)
    return render_template('search_note.html', results=[])

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8547, debug=False)
