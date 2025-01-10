from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}:{generate_password_hash(self.password)}\n")

    def validate_password(self, input_password: str) -> bool:
        return check_password_hash(self.password, input_password)

class Note:
    def __init__(self, username: str, title: str, content: str, note_id: int) -> None:
        self.username = username
        self.title = title
        self.content = content
        self.note_id = note_id

    def save(self) -> None:
        with open('notes.txt', 'a') as f:
            f.write(f"{self.username}|{self.title}|{self.content}|{self.note_id}\n")

    def delete(self) -> None:
        notes = []
        with open('notes.txt', 'r') as f:
            notes = f.readlines()
        with open('notes.txt', 'w') as f:
            for note in notes:
                if not note.startswith(f"{self.username}|{self.title}|{self.content}|{self.note_id}"):
                    f.write(note)

    def edit(self, title: str, content: str) -> None:
        self.title = title
        self.content = content
        self.delete()
        self.save()

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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        username = session['username']
        title = request.form['title']
        content = request.form['content']
        note_id = len(open('notes.txt').readlines()) + 1
        note = Note(username, title, content, note_id)
        note.save()
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<int:note_id>')
def view_note(note_id: int):
    notes = []
    with open('notes.txt', 'r') as f:
        notes = f.readlines()
    for note in notes:
        if note.endswith(f"|{note_id}\n"):
            note_data = note.strip().split('|')
            return render_template('view_note.html', note=note_data)
    return redirect(url_for('dashboard'))

@app.route('/search_notes', methods=['GET', 'POST'])
def search_notes():
    if request.method == 'POST':
        query = request.form['query']
        results = []
        with open('notes.txt', 'r') as f:
            notes = f.readlines()
            for note in notes:
                if query in note:
                    results.append(note.strip().split('|'))
        return render_template('search_note.html', results=results)
    return render_template('search_note.html')

if __name__ == '__main__':
    app.run(port=8358, debug=False)
