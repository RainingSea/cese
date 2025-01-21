from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from note import Note
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User()
        if user.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    note = Note(username)
    notes = note.get_notes()
    return render_template('dashboard.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note = Note(username)
        note.create_note(title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET'])
def view_note(title):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    note = Note(username)
    note_content = note.get_note_content(title)
    return render_template('view_note.html', title=title, content=note_content)

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    if request.method == 'POST':
        query = request.form['query']
        note = Note(username)
        results = note.search_notes(query)
        return render_template('search_note.html', results=results)
    return render_template('search_note.html', results=[])

if __name__ == '__main__':
    app.run(port=8960, debug=False)
