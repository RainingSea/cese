from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from note_manager import NoteManager

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
    return render_template('register.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    notes = note_manager.get_notes(session['username'])
    return render_template('dashboard.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager.add_note(title, content, session['username'])
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<note_id>', methods=['GET', 'POST'])
def view_note(note_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    note = note_manager.notes.get(note_id)
    if note is None or note['username'] != session['username']:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager.edit_note(note_id, title, content)
        return redirect(url_for('dashboard'))
    return render_template('view_note.html', note=note, note_id=note_id)

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        notes = note_manager.search_notes(title, session['username'])
        return render_template('search_note.html', notes=notes)
    return render_template('search_note.html', notes=[])

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
    user_manager.load_users()
    note_manager.load_notes()
    app.run(port=8361, debug=False)
