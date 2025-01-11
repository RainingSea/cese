from flask import Flask, render_template, request, redirect, session
from user import User
from note import Note

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = {}
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split(':')
                users[username] = password
    except FileNotFoundError:
        pass
    return users

def load_notes(username):
    notes = []
    try:
        with open(f'notes_{username}.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split(':')
                notes.append(Note(title, content))
    except FileNotFoundError:
        pass
    return notes

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('users.txt', 'a') as file:
            file.write(f'{username}:{password}\n')
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if username:
        notes = load_notes(username)
        return render_template('dashboard.html', notes=notes)
    return redirect('/')

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note = Note(title, content)
        note.save(session['username'])
        return redirect('/dashboard')
    return render_template('add_note.html')

@app.route('/view_note/<int:note_id>')
def view_note(note_id):
    username = session.get('username')
    notes = load_notes(username)
    if 0 <= note_id < len(notes):
        note = notes[note_id]
        return render_template('view_note.html', note=note)
    return redirect('/dashboard')

@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    username = session.get('username')
    notes = load_notes(username)
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        notes[note_id].edit(new_title, new_content)
        return redirect('/dashboard')
    note = notes[note_id]
    return render_template('add_note.html', title=note.title, content=note.content)

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    username = session.get('username')
    notes = load_notes(username)
    if 0 <= note_id < len(notes):
        notes[note_id].delete(username)
    return redirect('/dashboard')

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    username = session.get('username')
    notes = load_notes(username)
    if request.method == 'POST':
        search_term = request.form['search_term']
        filtered_notes = [note for note in notes if search_term in note.title]
        return render_template('search_note.html', notes=filtered_notes)
    return render_template('search_note.html', notes=notes)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8374, debug=False)
