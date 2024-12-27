from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self, filename):
        self.filename = filename
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')[:2]
                    self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if self.user_exists(username):
            return False
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users[username] = password
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def user_exists(self, username: str) -> bool:
        return username in self.users

class NoteManager:
    def __init__(self, username):
        self.filename = f'notes_{username}.txt'
        self.load_notes()

    def load_notes(self):
        self.notes = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    title, content = line.strip().split('|')
                    self.notes[title] = content

    def add_note(self, title: str, content: str) -> bool:
        if title in self.notes:
            return False
        with open(self.filename, 'a') as file:
            file.write(f"{title}|{content}\n")
        self.notes[title] = content
        return True

    def edit_note(self, old_title: str, new_title: str, new_content: str) -> bool:
        if old_title not in self.notes:
            return False
        del self.notes[old_title]
        self.add_note(new_title, new_content)
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
        return [(t, c) for t, c in self.notes.items() if title.lower() in t.lower()]

    def save_notes(self):
        with open(self.filename, 'w') as file:
            for title, content in self.notes.items():
                file.write(f"{title}|{content}\n")

user_manager = UserManager('users.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            if user_manager.register(username, password):
                return redirect(url_for('login'))
            else:
                return "Username already exists."
        else:
            return "Passwords do not match."
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    note_manager = NoteManager(session['username'])
    notes = note_manager.get_notes()
    return render_template('dashboard.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager = NoteManager(session['username'])
        if note_manager.add_note(title, content):
            return redirect(url_for('dashboard'))
        else:
            return "Note with this title already exists."
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET', 'POST'])
def view_note(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    note_manager = NoteManager(session['username'])
    if request.method == 'POST':
        if 'edit' in request.form:
            new_title = request.form['new_title']
            new_content = request.form['new_content']
            note_manager.edit_note(title, new_title, new_content)
            return redirect(url_for('dashboard'))
        elif 'delete' in request.form:
            note_manager.delete_note(title)
            return redirect(url_for('dashboard'))
    content = note_manager.notes.get(title, "")
    return render_template('view_note.html', title=title, content=content)

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    note_manager = NoteManager(session['username'])
    results = []
    if request.method == 'POST':
        title = request.form['title']
        results = note_manager.search_notes(title)
    return render_template('search_note.html', results=results)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)