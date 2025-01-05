from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self, username: str, password: str) -> bool:
        users = FileManager().read_users()
        if any(u[0] == username for u in users):
            return False
        FileManager().write_users(users + [[username, password]])
        return True

    def login(self, username: str, password: str) -> bool:
        users = FileManager().read_users()
        return any(u[0] == username and u[1] == password for u in users)


class Note:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def create(self, title: str, content: str) -> bool:
        notes = FileManager().read_notes()
        FileManager().write_notes(notes + [[title, content]])
        return True

    def edit(self, title: str, content: str) -> bool:
        notes = FileManager().read_notes()
        for note in notes:
            if note[0] == title:
                note[1] = content
                FileManager().write_notes(notes)
                return True
        return False

    def delete(self, title: str) -> bool:
        notes = FileManager().read_notes()
        notes = [note for note in notes if note[0] != title]
        FileManager().write_notes(notes)
        return True

    def search(self, title: str) -> list:
        notes = FileManager().read_notes()
        return [note for note in notes if title.lower() in note[0].lower()]


class FileManager:
    @staticmethod
    def read_users() -> list:
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                users.append(line.strip().split('|'))
        return users

    @staticmethod
    def write_users(users: list) -> None:
        with open('users.txt', 'w') as file:
            for user in users:
                file.write('|'.join(user) + '\n')

    @staticmethod
    def read_notes() -> list:
        notes = []
        with open('notes.txt', 'r') as file:
            for line in file:
                notes.append(line.strip().split('|'))
        return notes

    @staticmethod
    def write_notes(notes: list) -> None:
        with open('notes.txt', 'w') as file:
            for note in notes:
                file.write('|'.join(note) + '\n')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Login failed", 403
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Registration failed", 400
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    notes = FileManager().read_notes()
    return render_template('dashboard.html', notes=notes)


@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note = Note(title, content)
        note.create(title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')


@app.route('/view_note/<title>', methods=['GET', 'POST'])
def view_note(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    notes = FileManager().read_notes()
    note = next((n for n in notes if n[0] == title), None)
    if request.method == 'POST':
        if 'edit' in request.form:
            content = request.form['content']
            Note().edit(title, content)
            return redirect(url_for('dashboard'))
        if 'delete' in request.form:
            Note().delete(title)
            return redirect(url_for('dashboard'))
    return render_template('view_note.html', note=note)


@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        results = Note().search(title)
        return render_template('search_note.html', results=results)
    return render_template('search_note.html', results=[])


if __name__ == '__main__':
    app.run(port=8030, debug=False)
