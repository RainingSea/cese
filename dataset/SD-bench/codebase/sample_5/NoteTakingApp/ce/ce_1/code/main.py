from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> bool:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")
        return True

    def validate_password(self, password: str) -> bool:
        return self.password == password


class Note:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def to_string(self) -> str:
        return f"{self.title}|{self.content}"


def load_users() -> dict:
    users = {}
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users[username] = User(username, password)
    return users


def load_notes(username: str) -> list:
    notes = []
    notes_file = f'notes_{username}.txt'
    if os.path.exists(notes_file):
        with open(notes_file, 'r') as f:
            for line in f:
                title, content = line.strip().split('|')
                notes.append(Note(title, content))
    return notes


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username].validate_password(password):
            session['username'] = username
            return redirect(url_for('dashboard'))
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
    username = session.get('username')
    notes = load_notes(username)
    return render_template('dashboard.html', notes=notes)


@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        username = session.get('username')
        title = request.form['title']
        content = request.form['content']
        note = Note(title, content)
        with open(f'notes_{username}.txt', 'a') as f:
            f.write(note.to_string() + '\n')
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')


@app.route('/view_note/<title>', methods=['GET', 'POST'])
def view_note(title):
    username = session.get('username')
    notes = load_notes(username)
    note = next((n for n in notes if n.title == title), None)
    if request.method == 'POST':
        new_content = request.form['content']
        note.content = new_content
        with open(f'notes_{username}.txt', 'w') as f:
            for n in notes:
                f.write(n.to_string() + '\n')
        return redirect(url_for('dashboard'))
    return render_template('view_note.html', note=note)


@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if request.method == 'POST':
        username = session.get('username')
        query = request.form['query']
        notes = load_notes(username)
        filtered_notes = [n for n in notes if query.lower() in n.title.lower()]
        return render_template('search_note.html', notes=filtered_notes)
    return render_template('search_note.html', notes=[])


if __name__ == '__main__':
    app.run(port=8460, debug=False)
