from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self, username: str, password: str) -> bool:
        if self._is_username_taken(username):
            return False
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        users = self._load_users()
        return any(user.username == username and user.password == password for user in users)

    def _is_username_taken(self, username: str) -> bool:
        users = self._load_users()
        return any(user.username == username for user in users)

    def _load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

class Note:
    def __init__(self, username: str, title: str = '', content: str = ''):
        self.username = username
        self.title = title
        self.content = content

    def create_note(self, username: str, title: str, content: str) -> None:
        with open('notes.txt', 'a') as f:
            f.write(f"{username}|{title}|{content}\n")

    def view_notes(self, username: str) -> list:
        notes = []
        if os.path.exists('notes.txt'):
            with open('notes.txt', 'r') as f:
                for line in f:
                    note_data = line.strip().split('|')
                    if note_data[0] == username:
                        notes.append({'title': note_data[1], 'content': note_data[2]})
        return notes

    def edit_note(self, username: str, title: str, new_content: str) -> bool:
        notes = self.view_notes(username)
        updated = False
        with open('notes.txt', 'w') as f:
            for note in notes:
                if note['title'] == title:
                    f.write(f"{username}|{title}|{new_content}\n")
                    updated = True
                else:
                    f.write(f"{username}|{note['title']}|{note['content']}\n")
        return updated

    def delete_note(self, username: str, title: str) -> bool:
        notes = self.view_notes(username)
        updated = False
        with open('notes.txt', 'w') as f:
            for note in notes:
                if note['title'] != title:
                    f.write(f"{username}|{note['title']}|{note['content']}\n")
                else:
                    updated = True
        return updated

    def search_notes(self, username: str, title: str) -> list:
        results = []
        if os.path.exists('notes.txt'):
            with open('notes.txt', 'r') as f:
                for line in f:
                    note_data = line.strip().split('|')
                    if note_data[0] == username and title.lower() in note_data[1].lower():
                        results.append({'title': note_data[1], 'content': note_data[2]})
        return results

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
        else:
            return "Username already taken", 400
    return render_template('register.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    note = Note(session['username'])
    notes = note.view_notes(session['username'])
    return render_template('dashboard.html', username=session['username'], notes=notes)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    if user.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Invalid credentials", 401

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
        note = Note(session['username'])
        note.create_note(session['username'], title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note', methods=['GET', 'POST'])
def view_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    title = request.args.get('title')
    note = Note(session['username'])
    notes = note.view_notes(session['username'])
    current_note = next((n for n in notes if n['title'] == title), None)
    
    if request.method == 'POST':
        if 'edit' in request.form:
            new_content = request.form['content']
            note.edit_note(session['username'], title, new_content)
            return redirect(url_for('dashboard'))
        elif 'delete' in request.form:
            note.delete_note(session['username'], title)
            return redirect(url_for('dashboard'))

    return render_template('view_note.html', note=current_note)

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    results = []
    if request.method == 'POST':
        title = request.form['title']
        note = Note(session['username'])
        results = note.search_notes(session['username'], title)
    return render_template('search_note.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)