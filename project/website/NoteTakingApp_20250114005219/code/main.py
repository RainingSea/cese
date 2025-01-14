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

    def load(self) -> bool:
        if not os.path.exists('users.txt'):
            return False
        with open('users.txt', 'r') as f:
            users = f.readlines()
        for user in users:
            uname, pwd = user.strip().split('|')
            if uname == self.username and pwd == self.password:
                return True
        return False

class Note:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self, username: str) -> bool:
        with open(f'notes_{username}.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}\n")
        return True

    def load(self, username: str) -> list:
        if not os.path.exists(f'notes_{username}.txt'):
            return []
        with open(f'notes_{username}.txt', 'r') as f:
            notes = f.readlines()
        return [note.strip().split('|') for note in notes]

    def delete(self, username: str) -> bool:
        notes = self.load(username)
        notes = [note for note in notes if note[0] != self.title]
        with open(f'notes_{username}.txt', 'w') as f:
            for note in notes:
                f.write(f"{note[0]}|{note[1]}\n")
        return True

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
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    note = Note('', '')
    notes = note.load(username)
    return render_template('dashboard.html', notes=notes)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    if user.load():
        session['username'] = username
        return redirect(url_for('dashboard'))
    return 'Invalid credentials', 401

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note = Note(title, content)
        note.save(session['username'])
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET', 'POST'])
def view_note(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    note = Note(title, '')
    notes = note.load(session['username'])
    note_content = next((n[1] for n in notes if n[0] == title), None)
    if request.method == 'POST':
        new_content = request.form['content']
        note.content = new_content
        note.delete(session['username'])
        note.save(session['username'])
        return redirect(url_for('dashboard'))
    return render_template('view_note.html', title=title, content=note_content)

@app.route('/delete_note/<title>')
def delete_note(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    note = Note(title, '')
    note.delete(session['username'])
    return redirect(url_for('dashboard'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        query = request.form['query']
        note = Note('', '')
        notes = note.load(session['username'])
        filtered_notes = [n for n in notes if query.lower() in n[0].lower()]
        return render_template('search_note.html', notes=filtered_notes)
    return render_template('search_note.html', notes=[])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8459, debug=False)
