from flask import Flask, render_template, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

class NoteTakingApp:
    def __init__(self):
        self.users = self.load_users()
        self.notes = self.load_notes()

    def load_users(self):
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split(',')
                    users[username] = password
        return users

    def load_notes(self):
        notes = {}
        if os.path.exists('notes.txt'):
            with open('notes.txt', 'r') as f:
                for line in f:
                    username, title, content = line.strip().split(',', 2)
                    if username not in notes:
                        notes[username] = []
                    notes[username].append({'title': title, 'content': content})
        return notes

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as f:
            f.write(f"{username},{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def add_note(self, username: str, title: str, content: str) -> bool:
        if username not in self.notes:
            self.notes[username] = []
        self.notes[username].append({'title': title, 'content': content})
        with open('notes.txt', 'a') as f:
            f.write(f"{username},{title},{content}\n")
        return True

    def view_notes(self, username: str) -> list:
        return self.notes.get(username, [])

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
        return [note for note in self.notes.get(username, []) if title.lower() in note['title'].lower()]

    def save_notes(self):
        with open('notes.txt', 'w') as f:
            for username, notes in self.notes.items():
                for note in notes:
                    f.write(f"{username},{note['title']},{note['content']}\n")

app_instance = NoteTakingApp()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app_instance.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app_instance.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    notes = app_instance.view_notes(username)
    return render_template('dashboard.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        app_instance.add_note(username, title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>')
def view_note(title):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    notes = app_instance.view_notes(username)
    note = next((note for note in notes if note['title'] == title), None)
    return render_template('view_note.html', note=note)

@app.route('/edit_note/<title>', methods=['GET', 'POST'])
def edit_note(title):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_content = request.form['content']
        app_instance.edit_note(username, title, new_content)
        return redirect(url_for('dashboard'))
    note = next((note for note in app_instance.view_notes(username) if note['title'] == title), None)
    return render_template('edit_note.html', note=note)

@app.route('/delete_note/<title>', methods=['POST'])
def delete_note(title):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    app_instance.delete_note(username, title)
    return redirect(url_for('dashboard'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    results = []
    if request.method == 'POST':
        title = request.form['title']
        results = app_instance.search_notes(username, title)
    return render_template('search_note.html', results=results)

if __name__ == '__main__':
    app.run(port=8958, debug=False)
