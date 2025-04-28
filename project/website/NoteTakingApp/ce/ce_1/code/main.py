from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from note_manager import NoteManager
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
note_manager = NoteManager()

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
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' in session:
        notes = note_manager.get_notes(session['username'])
        return render_template('dashboard.html', notes=notes)
    return redirect(url_for('login'))

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager.add_note(title, content, session['username'])
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<int:note_id>', methods=['GET', 'POST'])
def view_note(note_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager.edit_note(note_id, title, content)
        return redirect(url_for('dashboard'))
    note = note_manager.notes.get(note_id)
    return render_template('view_note.html', note=note)

@app.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    note_manager.delete_note(note_id)
    return redirect(url_for('dashboard'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if request.method == 'POST':
        query = request.form['query']
        results = note_manager.search_notes(query, session['username'])
        return render_template('search_note.html', results=results)
    return render_template('search_note.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8359, debug=False)
