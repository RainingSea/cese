from flask import Flask, render_template, redirect, url_for, request, session
from user_manager import UserManager
from note_manager import NoteManager
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

user_manager = UserManager()
note_manager = NoteManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    note_manager.username = session['username']
    notes = note_manager.get_notes()
    return render_template('dashboard.html', notes=notes)

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
        note_manager.add_note(title, content)
        return redirect(url_for('dashboard'))
    
    return render_template('add_note.html')

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    note_manager.username = session['username']
    search_results = []
    
    if request.method == 'POST':
        query = request.form['query']
        search_results = note_manager.search_notes(query)
    
    return render_template('search_note.html', results=search_results)

@app.route('/view_note/<int:note_id>', methods=['GET', 'POST'])
def view_note(note_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    note_manager.username = session['username']
    
    if request.method == 'POST':
        if 'edit' in request.form:
            title = request.form['title']
            content = request.form['content']
            note_manager.edit_note(note_id, title, content)
            return redirect(url_for('dashboard'))
        elif 'delete' in request.form:
            note_manager.delete_note(note_id)
            return redirect(url_for('dashboard'))
    
    note = note_manager.get_note_by_id(note_id)
    return render_template('view_note.html', note=note)

if __name__ == '__main__':
    user_manager.load_users()
    app.run(port=8174, debug=True)
