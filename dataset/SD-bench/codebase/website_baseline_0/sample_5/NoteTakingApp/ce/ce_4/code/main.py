from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self, username: str, password: str) -> bool:
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

class Note:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def create_note(self, title: str, content: str) -> None:
        with open(f'notes_{session["username"]}.txt', 'a') as f:
            f.write(f"{title}|{content}\n")

    def edit_note(self, old_title: str, new_title: str, new_content: str) -> None:
        notes = []
        with open(f'notes_{session["username"]}.txt', 'r') as f:
            notes = f.readlines()
        with open(f'notes_{session["username"]}.txt', 'w') as f:
            for note in notes:
                if note.startswith(old_title):
                    f.write(f"{new_title}|{new_content}\n")
                else:
                    f.write(note)

    def delete_note(self, title: str) -> None:
        notes = []
        with open(f'notes_{session["username"]}.txt', 'r') as f:
            notes = f.readlines()
        with open(f'notes_{session["username"]}.txt', 'w') as f:
            for note in notes:
                if not note.startswith(title):
                    f.write(note)

class NoteManager:
    def load_notes(self, username: str) -> list:
        notes = []
        if os.path.exists(f'notes_{username}.txt'):
            with open(f'notes_{username}.txt', 'r') as f:
                notes = [line.strip().split('|') for line in f.readlines()]
        return notes

    def save_notes(self, username: str) -> None:
        pass  # Not needed as notes are saved immediately

    def search_notes(self, username: str, query: str) -> list:
        notes = self.load_notes(username)
        return [note for note in notes if query.lower() in note[0].lower()]

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.register(username, password)
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    note_manager = NoteManager()
    notes = note_manager.load_notes(session['username'])
    return render_template('dashboard.html', notes=notes)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    if user.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return redirect('/')

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note = Note(title, content)
        note.create_note(title, content)
        return redirect('/dashboard')
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET', 'POST'])
def view_note(title):
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        note = Note(title, '')
        note.edit_note(title, new_title, new_content)
        return redirect('/dashboard')
    
    note_manager = NoteManager()
    notes = note_manager.load_notes(session['username'])
    note_content = next((note[1] for note in notes if note[0] == title), None)
    return render_template('view_note.html', title=title, content=note_content)

@app.route('/delete_note/<title>')
def delete_note(title):
    note = Note(title, '')
    note.delete_note(title)
    return redirect('/dashboard')

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if request.method == 'POST':
        query = request.form['query']
        note_manager = NoteManager()
        results = note_manager.search_notes(session['username'], query)
        return render_template('search_note.html', results=results)
    return render_template('search_note.html', results=[])

if __name__ == '__main__':
    app.run(port=8463, debug=False)
