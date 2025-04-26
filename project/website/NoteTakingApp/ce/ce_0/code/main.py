from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class NoteManager:
    def __init__(self, notes_dir: str):
        self.notes_dir = notes_dir
        if not os.path.exists(self.notes_dir):
            os.makedirs(self.notes_dir)

    def _get_notes_file(self, username: str) -> str:
        return os.path.join(self.notes_dir, f"{username}_notes.txt")

    def add_note(self, username: str, title: str, content: str) -> bool:
        notes_file = self._get_notes_file(username)
        with open(notes_file, 'a') as file:
            file.write(f"{title}|{content}\n")
        return True

    def edit_note(self, username: str, title: str, new_content: str) -> bool:
        notes_file = self._get_notes_file(username)
        if not os.path.exists(notes_file):
            return False

        notes = []
        with open(notes_file, 'r') as file:
            notes = [line.strip().split('|') for line in file]

        for note in notes:
            if note[0] == title:
                note[1] = new_content
                break

        with open(notes_file, 'w') as file:
            for note in notes:
                file.write(f"{note[0]}|{note[1]}\n")
        return True

    def delete_note(self, username: str, title: str) -> bool:
        notes_file = self._get_notes_file(username)
        if not os.path.exists(notes_file):
            return False

        notes = []
        with open(notes_file, 'r') as file:
            notes = [line.strip().split('|') for line in file]

        notes = [note for note in notes if note[0] != title]

        with open(notes_file, 'w') as file:
            for note in notes:
                file.write(f"{note[0]}|{note[1]}\n")
        return True

    def get_notes(self, username: str) -> list:
        notes_file = self._get_notes_file(username)
        if not os.path.exists(notes_file):
            return []
        with open(notes_file, 'r') as file:
            return [line.strip().split('|') for line in file]

    def search_notes(self, username: str, query: str) -> list:
        notes = self.get_notes(username)
        return [note for note in notes if query.lower() in note[0].lower()]

user_manager = UserManager('users.txt')
note_manager = NoteManager('notes')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    notes = note_manager.get_notes(username)
    return render_template('dashboard.html', notes=notes)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager.add_note(session['username'], title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET'])
def view_note(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    notes = note_manager.get_notes(session['username'])
    note_content = next((note[1] for note in notes if note[0] == title), None)
    return render_template('view_note.html', title=title, content=note_content)

@app.route('/edit_note/<title>', methods=['GET', 'POST'])
def edit_note(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_content = request.form['content']
        note_manager.edit_note(session['username'], title, new_content)
        return redirect(url_for('dashboard'))
    notes = note_manager.get_notes(session['username'])
    note_content = next((note[1] for note in notes if note[0] == title), None)
    return render_template('add_note.html', title=title, content=note_content)

@app.route('/delete_note/<title>', methods=['POST'])
def delete_note(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    note_manager.delete_note(session['username'], title)
    return redirect(url_for('dashboard'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        query = request.form['query']
        results = note_manager.search_notes(session['username'], query)
        return render_template('search_note.html', results=results)
    return render_template('search_note.html', results=[])

if __name__ == '__main__':
    app.run(port=8194, debug=False)
