from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from note import Note
from auth import Auth
from note_manager import NoteManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and notes from files
user_manager = User()
note_manager = NoteManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Auth().register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', notes=note_manager.load_notes())

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager.add_note(Note(title, content))
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET', 'POST'])
def view_note(title):
    note = note_manager.load_notes()
    for n in note:
        if n.title == title:
            if request.method == 'POST':
                new_content = request.form['content']
                note_manager.edit_note(title, new_content)
                return redirect(url_for('dashboard'))
            return render_template('view_note.html', note=n)
    return redirect(url_for('dashboard'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if request.method == 'POST':
        query = request.form['query']
        results = note_manager.search_notes(query)
        return render_template('search_note.html', results=results)
    return render_template('search_note.html', results=[])

if __name__ == '__main__':
    app.run(port=8959, debug=False)
