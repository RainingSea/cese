from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self, username: str, password: str) -> bool:
        if not self.user_exists(username):
            with open('users.txt', 'a') as f:
                f.write(f"{username}|{password}\n")
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

    def user_exists(self, username: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                stored_username, _ = line.strip().split('|')
                if stored_username == username:
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
            'user': self.user
        }
        with open('notes.txt', 'a') as f:
            f.write(json.dumps(note_data) + '\n')
        return True

    def edit_note(self, title: str, content: str) -> bool:
        notes = self.load_notes()
        for note in notes:
            if note['title'] == title and note['user'] == self.user:
                note['content'] = content
                self.save_notes(notes)
                return True
        return False

    def delete_note(self, title: str) -> bool:
        notes = self.load_notes()
        notes = [note for note in notes if not (note['title'] == title and note['user'] == self.user)]
        self.save_notes(notes)
        return True

    def search_notes(self, title: str) -> list:
        notes = self.load_notes()
        return [note for note in notes if title.lower() in note['title'].lower() and note['user'] == self.user]

    def load_notes(self) -> list:
        if not os.path.exists('notes.txt'):
            return []
        with open('notes.txt', 'r') as f:
            return [json.loads(line.strip()) for line in f]

    def save_notes(self, notes: list) -> None:
        with open('notes.txt', 'w') as f:
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
        return "User already exists!"
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    if user.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login', error='Invalid credentials'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    notes = Note.load_notes(Note('', '', session['username']))  # Load notes for the logged-in user
    return render_template('dashboard.html', username=session['username'], notes=notes)

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
    notes = Note.load_notes(Note('', '', session['username']))
    note = next((note for note in notes if note['title'] == title), None)
    if request.method == 'POST':
        content = request.form['content']
        note_obj = Note(title, content, session['username'])
        note_obj.edit_note(title, content)
        return redirect(url_for('dashboard'))
    return render_template('view_note.html', note=note)

@app.route('/delete_note/<title>', methods=['POST'])
def delete_note(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    note = Note('', '', session['username'])
    note.delete_note(title)
    return redirect(url_for('dashboard'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        note = Note('', '', session['username'])
        results = note.search_notes(title)
        return render_template('search_note.html', results=results)
    return render_template('search_note.html', results=[])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8134, debug=True)
