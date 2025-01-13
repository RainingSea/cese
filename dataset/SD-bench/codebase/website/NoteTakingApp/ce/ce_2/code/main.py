from flask import Flask, render_template, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class Main:
    def __init__(self):
        self.users_file = 'users.txt'
        self.notes_file = 'notes.txt'
        self.load_data()

    def load_data(self):
        self.users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    self.users[username] = password

        self.notes = {}
        if os.path.exists(self.notes_file):
            with open(self.notes_file, 'r') as f:
                for line in f:
                    username, note_title, note_content = line.strip().split('|')
                    if username not in self.notes:
                        self.notes[username] = []
                    self.notes[username].append({'title': note_title, 'content': note_content})

    def register_user(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login_user(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def add_note(self, username: str, title: str, content: str) -> bool:
        if username not in self.notes:
            self.notes[username] = []
        self.notes[username].append({'title': title, 'content': content})
        with open(self.notes_file, 'a') as f:
            f.write(f"{username}|{title}|{content}\n")
        return True

    def get_notes(self, username: str) -> list:
        return self.notes.get(username, [])

    def get_note_details(self, username: str, title: str) -> dict:
        for note in self.notes.get(username, []):
            if note['title'] == title:
                return note
        return {}

    def edit_note(self, username: str, title: str, new_content: str) -> bool:
        for note in self.notes.get(username, []):
            if note['title'] == title:
                note['content'] = new_content
                self.save_notes()
                return True
        return False

    def delete_note(self, username: str, title: str) -> bool:
        if username in self.notes:
            self.notes[username] = [note for note in self.notes[username] if note['title'] != title]
            self.save_notes()
            return True
        return False

    def search_notes(self, username: str, title: str) -> list:
        return [note for note in self.notes.get(username, []) if title in note['title']]

    def save_notes(self):
        with open(self.notes_file, 'w') as f:
            for username, notes in self.notes.items():
                for note in notes:
                    f.write(f"{username}|{note['title']}|{note['content']}\n")

main_app = Main()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if main_app.register_user(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if username:
        notes = main_app.get_notes(username)
        return render_template('dashboard.html', notes=notes)
    return redirect(url_for('login'))

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    username = session.get('username')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        main_app.add_note(username, title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET', 'POST'])
def view_note(title):
    username = session.get('username')
    if request.method == 'POST':
        new_content = request.form['content']
        main_app.edit_note(username, title, new_content)
        return redirect(url_for('dashboard'))
    note = main_app.get_note_details(username, title)
    return render_template('view_note.html', note=note)

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    username = session.get('username')
    if request.method == 'POST':
        title = request.form['title']
        results = main_app.search_notes(username, title)
        return render_template('search_note.html', results=results)
    return render_template('search_note.html', results=[])

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if main_app.login_user(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8461, debug=False)
