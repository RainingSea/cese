from flask import Flask, render_template, request, redirect, session
from user import User
from note import Note
from note_manager import NoteManager
from file_manager import FileManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

file_manager = FileManager()
note_manager = NoteManager()

def load_users() -> dict:
    """Load users from the users.txt file."""
    users_data = file_manager.read_file('users.txt')
    users = {}
    for line in users_data:
        username, password = line.strip().split('|')
        users[username] = User(username, password)
    return users

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username].validate_password(password):
            session['username'] = username
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Display the user dashboard with their notes."""
    if 'username' not in session:
        return redirect('/')
    notes = note_manager.load_notes(session['username'])
    return render_template('dashboard.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    """Add a new note for the logged-in user."""
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note = Note(title, content, session['username'])
        note_manager.add_note(note)
        return redirect('/dashboard')
    return render_template('add_note.html')

@app.route('/view_note/<title>')
def view_note(title):
    """View a specific note by title."""
    if 'username' not in session:
        return redirect('/')
    notes = note_manager.load_notes(session['username'])
    note = next((note for note in notes if note.title == title), None)
    if note is None:
        return redirect('/dashboard')  # Redirect if note not found
    return render_template('view_note.html', note=note)

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    """Search for notes by title."""
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        notes = note_manager.search_notes(title)
        return render_template('search_note.html', notes=notes)
    return render_template('search_note.html', notes=[])

@app.route('/edit_note/<title>', methods=['GET', 'POST'])
def edit_note(title):
    """Edit an existing note."""
    if 'username' not in session:
        return redirect('/')
    notes = note_manager.load_notes(session['username'])
    note = next((note for note in notes if note.title == title), None)
    if note is None:
        return redirect('/dashboard')  # Redirect if note not found
    if request.method == 'POST':
        new_content = request.form['content']
        note_manager.edit_note(title, new_content)
        return redirect('/dashboard')
    return render_template('edit_note.html', note=note)

@app.route('/logout')
def logout():
    """Log out the user."""
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8464, debug=False)
