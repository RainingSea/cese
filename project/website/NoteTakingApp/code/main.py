from flask import Flask, render_template, request, redirect, session, flash
from user import User, AuthManager
from note import NoteManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

auth_manager = AuthManager()
note_manager = None

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_manager.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
        flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect('/')
        flash('Username already exists.')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Displays the user dashboard with notes."""
    username = session.get('username')
    if username:
        global note_manager
        note_manager = NoteManager(username)
        note_manager.load_notes()
        notes = note_manager.get_notes()
        return render_template('dashboard.html', notes=notes)
    flash('You need to log in first.')
    return redirect('/')

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    """Handles adding a new note."""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager.add_note(title, content)
        flash('Note added successfully.')
        return redirect('/dashboard')
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET', 'POST'])
def view_note(title):
    """Handles viewing and editing a specific note."""
    note = note_manager.find_note_by_title(title)
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        if note:
            note.edit(new_title, new_content)
            note_manager.save_notes()
            flash('Note updated successfully.')
        else:
            flash('Note not found.')
        return redirect('/dashboard')
    return render_template('view_note.html', note=note)

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    """Handles searching for a note by title."""
    note = None
    if request.method == 'POST':
        title = request.form['title']
        note = note_manager.find_note_by_title(title)
        if note is None:
            flash('No note found with that title.')
    return render_template('search_note.html', note=note)

@app.route('/logout')
def logout():
    """Handles user logout."""
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8375, debug=False)
