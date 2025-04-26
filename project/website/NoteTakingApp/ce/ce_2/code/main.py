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
                    username, password = line.strip().split(':')
                    self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        with open(self.users_file, 'a') as file:
            file.write(f"{username}:{password}\n")
        self.users[username] = password
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class NoteManager:
    def __init__(self, notes_file: str):
        self.notes_file = notes_file
        self.load_notes()

    def load_notes(self):
        self.notes = {}
        if os.path.exists(self.notes_file):
            with open(self.notes_file, 'r') as file:
                for line in file:
                    title, content = line.strip().split('|')
                    self.notes[title] = content

    def add_note(self, title: str, content: str) -> bool:
        if title in self.notes:
            return False
        with open(self.notes_file, 'a') as file:
            file.write(f"{title}|{content}\n")
        self.notes[title] = content
        return True

    def edit_note(self, title: str, new_content: str) -> bool:
        if title not in self.notes:
            return False
        self.notes[title] = new_content
        self.save_notes()
        return True

    def delete_note(self, title: str) -> bool:
        if title not in self.notes:
            return False
        del self.notes[title]
        self.save_notes()
        return True

    def get_notes(self) -> list:
        return list(self.notes.items())

    def search_notes(self, title: str) -> list:
        return [(t, c) for t, c in self.notes.items() if title in t]

    def save_notes(self):
        with open(self.notes_file, 'w') as file:
            for title, content in self.notes.items():
                file.write(f"{title}|{content}\n")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.register(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    notes = note_manager.get_notes()
    return render_template('dashboard.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager.add_note(title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>')
def view_note(title):
    content = note_manager.notes.get(title, '')
    return render_template('view_note.html', title=title, content=content)

@app.route('/edit_note/<title>', methods=['GET', 'POST'])
def edit_note(title):
    if request.method == 'POST':
        new_content = request.form['content']
        note_manager.edit_note(title, new_content)
        return redirect(url_for('dashboard'))
    content = note_manager.notes.get(title, '')
    return render_template('add_note.html', title=title, content=content)

@app.route('/delete_note/<title>')
def delete_note(title):
    note_manager.delete_note(title)
    return redirect(url_for('dashboard'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    results = []
    if request.method == 'POST':
        title = request.form['title']
        results = note_manager.search_notes(title)
    return render_template('search_note.html', results=results)

if __name__ == '__main__':
    user_manager = UserManager('users.txt')
    note_manager = NoteManager('notes.txt')
    app.run(port=8196, debug=False)
