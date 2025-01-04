from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# File paths
USERS_FILE = 'users.txt'
NOTES_FILE = 'notes.txt'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self, username: str, password: str) -> bool:
        if not self.user_exists(username):
            with open(USERS_FILE, 'a') as f:
                f.write(f"{username}|{password}\n")
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        with open(USERS_FILE, 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username and user_data[1] == password:
                    return True
        return False

    def user_exists(self, username: str) -> bool:
        with open(USERS_FILE, 'r') as f:
            for line in f:
                if line.startswith(username):
                    return True
        return False

class Note:
    def __init__(self, title: str, content: str, user: str):
        self.title = title
        self.content = content
        self.user = user

    def create_note(self, title: str, content: str) -> bool:
        note_data = {
            'title': title,
            'content': content,
            'user': session['username']
        }
        with open(NOTES_FILE, 'a') as f:
            f.write(json.dumps(note_data) + '\n')
        return True

    def edit_note(self, title: str, content: str) -> bool:
        notes = self.load_notes()
        for note in notes:
            if note['title'] == title and note['user'] == session['username']:
                note['content'] = content
                self.save_notes(notes)
                return True
        return False

    def delete_note(self, title: str) -> bool:
        notes = self.load_notes()
        notes = [note for note in notes if not (note['title'] == title and note['user'] == session['username'])]
        self.save_notes(notes)
        return True

    def search_notes(self, title: str) -> list:
        notes = self.load_notes()
        return [note for note in notes if title.lower() in note['title'].lower() and note['user'] == session['username']]

    def load_notes(self) -> list:
        if not os.path.exists(NOTES_FILE):
            return []
        with open(NOTES_FILE, 'r') as f:
            return [json.loads(line.strip()) for line in f]

    def save_notes(self, notes: list) -> None:
        with open(NOTES_FILE, 'w') as f:
            for note in notes:
                f.write(json.dumps(note) + '\n')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    notes = Note('', '', session['username']).load_notes()
    return render_template('dashboard.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note = Note(title, content, session['username'])
        note.create_note(title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET', 'POST'])
def view_note(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    notes = Note('', '', session['username']).load_notes()
    note = next((note for note in notes if note['title'] == title), None)
    if request.method == 'POST':
        content = request.form['content']
        Note('', '', session['username']).edit_note(title, content)
        return redirect(url_for('dashboard'))
    return render_template('view_note.html', note=note)

@app.route('/delete_note/<title>')
def delete_note(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    Note('', '', session['username']).delete_note(title)
    return redirect(url_for('dashboard'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        results = Note('', '', session['username']).search_notes(title)
        return render_template('search_note.html', results=results)
    return render_template('search_note.html', results=[])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8133, debug=True)
