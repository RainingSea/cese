from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from note_manager import NoteManager
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.json')
note_manager = NoteManager('notes.json')

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="Username already exists.")
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Displays the user's dashboard with their notes."""
    if 'username' not in session:
        return redirect(url_for('login'))
    notes = note_manager.get_notes(session['username'])
    return render_template('dashboard.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    """Handles adding a new note."""
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager.add_note(title, content, session['username'])
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<int:note_id>', methods=['GET', 'POST'])
def view_note(note_id):
    """Handles viewing and editing a specific note."""
    if 'username' not in session:
        return redirect(url_for('login'))
    notes = note_manager.get_notes(session['username'])
    if note_id < 0 or note_id >= len(notes):
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager.edit_note(note_id, title, content)
        return redirect(url_for('dashboard'))
    note = notes[note_id]
    return render_template('view_note.html', note=note)

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    """Handles deleting a specific note."""
    if 'username' not in session:
        return redirect(url_for('login'))
    note_manager.delete_note(note_id)
    return redirect(url_for('dashboard'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    """Handles searching for notes by title."""
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        results = note_manager.search_notes(title, session['username'])
        return render_template('search_note.html', results=results)
    return render_template('search_note.html', results=[])

if __name__ == '__main__':
    app.run(port=8360, debug=False)
