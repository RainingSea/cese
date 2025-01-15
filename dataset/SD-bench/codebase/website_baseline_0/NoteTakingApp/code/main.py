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
    if username:
        notes = Note().load_notes(username)
        return render_template('dashboard.html', notes=notes)
    return redirect(url_for('login'))

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    username = session.get('username')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note = Note(title, content)
        note.save(username)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET', 'POST'])
def view_note(title):
    username = session.get('username')
    note = Note().search(title, username)
    if not note:
        return "Note not found", 404
    if request.method == 'POST':
        new_title = request.form['new_title']
        new_content = request.form['new_content']
        note[0].edit(new_title, new_content, username)
        return redirect(url_for('dashboard'))
    return render_template('view_note.html', note=note[0])

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    username = session.get('username')
    if request.method == 'POST':
        title = request.form['title']
        notes = Note().search(title, username)
        return render_template('search_note.html', notes=notes)
    return render_template('search_note.html', notes=[])

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User()
    if user.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/delete_note/<title>', methods=['POST'])
def delete_note(title):
    username = session.get('username')
    if username:
        note = Note().search(title, username)
        if note:
            note[0].delete(username)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=8541, debug=False)
