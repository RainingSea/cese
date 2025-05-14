from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key_placeholder'

class FileStorage:
    def __init__(self):
        self.users_file = 'users.txt'
        self.notes_dir = 'user_notes'
        os.makedirs(self.notes_dir, exist_ok=True)

    def load_users(self):
        users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def save_users(self, users):
        with open(self.users_file, 'w') as f:
            for username, password in users.items():
                f.write(f"{username}|{password}\n")

    def load_notes(self, username):
        notes_file = os.path.join(self.notes_dir, f"notes_{username}.txt")
        if os.path.exists(notes_file):
            with open(notes_file, 'r') as f:
                return json.load(f)
        return {}

    def save_notes(self, username, notes):
        notes_file = os.path.join(self.notes_dir, f"notes_{username}.txt")
        with open(notes_file, 'w') as f:
            json.dump(notes, f)

class NoteTakingApp:
    def __init__(self):
        self.storage = FileStorage()
        self.current_user = None
        self.notes = {}

    def login(self, username, password):
        users = self.storage.load_users()
        if username in users and users[username] == password:
            self.current_user = username
            self.notes = self.storage.load_notes(username)
            return True
        return False

    def register(self, username, password, confirm_password):
        if password != confirm_password:
            return False
        users = self.storage.load_users()
        if username in users:
            return False
        users[username] = password
        self.storage.save_users(users)
        return True

    def add_note(self, title, content):
        if not self.current_user:
            return False
        note_id = str(datetime.now().timestamp())
        self.notes[note_id] = {
            'title': title,
            'content': content,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.storage.save_notes(self.current_user, self.notes)
        return True

    def view_note(self, note_id):
        return self.notes.get(note_id)

    def edit_note(self, note_id, title, content):
        if note_id in self.notes:
            self.notes[note_id]['title'] = title
            self.notes[note_id]['content'] = content
            self.storage.save_notes(self.current_user, self.notes)
            return True
        return False

    def delete_note(self, note_id):
        if note_id in self.notes:
            del self.notes[note_id]
            self.storage.save_notes(self.current_user, self.notes)
            return True
        return False

    def search_notes(self, query):
        results = []
        for note_id, note in self.notes.items():
            if query.lower() in note['title'].lower() or query.lower() in note['content'].lower():
                results.append((note_id, note))
        return results

    def logout(self):
        self.current_user = None
        self.notes = {}

note_app = NoteTakingApp()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if note_app.login(username, password):
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if note_app.register(username, password, confirm_password):
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        flash('Registration failed. Username may exist or passwords do not match.')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if not note_app.current_user:
        return redirect(url_for('login'))
    return render_template('dashboard.html', notes=note_app.notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if not note_app.current_user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if title and content:
            note_app.add_note(title, content)
            return redirect(url_for('dashboard'))
        flash('Title and content cannot be empty')
    return render_template('add_note.html')

@app.route('/view_note/<note_id>', methods=['GET', 'POST'])
def view_note(note_id):
    if not note_app.current_user:
        return redirect(url_for('login'))
    note = note_app.view_note(note_id)
    if not note:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        if 'delete' in request.form:
            note_app.delete_note(note_id)
            return redirect(url_for('dashboard'))
        elif 'edit' in request.form:
            title = request.form['title']
            content = request.form['content']
            if title and content:
                note_app.edit_note(note_id, title, content)
                return redirect(url_for('view_note', note_id=note_id))
            flash('Title and content cannot be empty')
    
    return render_template('view_note.html', note_id=note_id, note=note)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if not note_app.current_user:
        return redirect(url_for('login'))
    results = []
    if request.method == 'POST':
        query = request.form['query']
        results = note_app.search_notes(query)
    return render_template('search_note.html', results=results)

@app.route('/logout')
def logout():
    note_app.logout()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8094, debug=False)
