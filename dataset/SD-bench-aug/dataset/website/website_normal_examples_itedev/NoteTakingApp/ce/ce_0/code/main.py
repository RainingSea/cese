from flask import Flask, render_template, redirect, url_for, request, session
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
                user_data = line.strip().split('|')
                if user_data[0] == username and user_data[1] == password:
                    return True
        return False

class Note:
    def __init__(self, username: str, title: str = '', content: str = ''):
        self.username = username
        self.title = title
        self.content = content

    def create_note(self, username: str, title: str, content: str) -> None:
        with open('notes.txt', 'a') as f:
            f.write(f"{username}|{title}|{content}\n")

    def view_notes(self, username: str):
        notes = []
        with open('notes.txt', 'r') as f:
            for line in f:
                note_data = line.strip().split('|')
                if note_data[0] == username:
                    notes.append({'title': note_data[1], 'content': note_data[2]})
        return notes

    def edit_note(self, title: str, new_content: str) -> None:
        notes = []
        with open('notes.txt', 'r') as f:
            for line in f:
                note_data = line.strip().split('|')
                if note_data[0] == self.username and note_data[1] == title:
                    notes.append(f"{self.username}|{title}|{new_content}\n")
                else:
                    notes.append(line)
        with open('notes.txt', 'w') as f:
            f.writelines(notes)

    def delete_note(self, title: str) -> None:
        notes = []
        with open('notes.txt', 'r') as f:
            for line in f:
                note_data = line.strip().split('|')
                if not (note_data[0] == self.username and note_data[1] == title):
                    notes.append(line)
        with open('notes.txt', 'w') as f:
            f.writelines(notes)

    def search_notes(self, username: str, title: str):
        results = []
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
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            user = User(username, password)
            user.register(username, password)
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_notes = Note(username=session['username']).view_notes(session['username'])
    return render_template('dashboard.html', notes=user_notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note = Note(username=session['username'])
        note.create_note(session['username'], title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET', 'POST'])
def view_note(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    note = Note(username=session['username'])
    notes = note.view_notes(session['username'])
    current_note = next((n for n in notes if n['title'] == title), None)
    if request.method == 'POST':
        if 'edit' in request.form:
            new_content = request.form['content']
            note.edit_note(title, new_content)
            return redirect(url_for('dashboard'))
        elif 'delete' in request.form:
            note.delete_note(title)
            return redirect(url_for('dashboard'))
    return render_template('view_note.html', note=current_note)

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    search_results = []
    if request.method == 'POST':
        title = request.form['title']
        note = Note(username=session['username'])
        search_results = note.search_notes(session['username'], title)
    return render_template('search_note.html', results=search_results)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)