from flask import Flask, render_template, request, redirect, session, flash
from user_manager import UserManager
from note_manager import NoteManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
note_manager = NoteManager('notes.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect('/')
        else:
            flash('Username already exists.')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Displays the user dashboard with their notes."""
    if 'username' not in session:
        return redirect('/')
    notes = note_manager.get_notes(session['username'])
    return render_template('dashboard.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    """Handles adding a new note."""
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager.add_note(title, content, session['username'])
        return redirect('/dashboard')
    return render_template('add_note.html')

@app.route('/view_note/<int:note_id>', methods=['GET', 'POST'])
def view_note(note_id):
    """Handles viewing and editing a specific note."""
    if 'username' not in session:
        return redirect('/')
    note = note_manager.get_note_details(note_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager.edit_note(note_id, title, content)
        return redirect('/dashboard')
    return render_template('view_note.html', note=note)

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    """Handles deleting a specific note."""
    if 'username' not in session:
        return redirect('/')
    note_manager.delete_note(note_id)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    """Logs out the user."""
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8312, debug=False)
