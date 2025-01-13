from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from note_manager import NoteManager
import os
import logging

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a random secret key for security

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

user_manager = UserManager('users.txt')
note_manager = NoteManager('notes.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        notes = note_manager.get_notes(session['username'])
        return render_template('dashboard.html', notes=notes)
    return redirect(url_for('login'))

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' in session:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            note_manager.add_note(session['username'], title, content)
            return redirect(url_for('dashboard'))
        return render_template('add_note.html')
    return redirect(url_for('login'))

@app.route('/view_note/<title>', methods=['GET', 'POST'])
def view_note(title):
    if 'username' in session:
        if request.method == 'POST':
            new_content = request.form['content']
            note_manager.edit_note(session['username'], title, new_content)
            return redirect(url_for('dashboard'))
        note = note_manager.get_note_by_title(session['username'], title)
        return render_template('view_note.html', note=note)
    return redirect(url_for('login'))

@app.route('/delete_note/<title>', methods=['POST'])
def delete_note(title):
    if 'username' in session:
        note_manager.delete_note(session['username'], title)
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if 'username' in session:
        if request.method == 'POST':
            title = request.form['title']
            results = note_manager.search_notes(session['username'], title)
            return render_template('search_note.html', results=results)
        return render_template('search_note.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/health')
def health_check():
    return 'OK', 200  # Health check endpoint

if __name__ == '__main__':
    try:
        app.run(port=8071, debug=False)
    except Exception as e:
        logging.error(f"Application failed to start: {e}")
        exit(1)