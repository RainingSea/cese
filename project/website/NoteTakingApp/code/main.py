from flask import Flask, render_template, request, redirect, session, flash
from user_manager import UserManager
from note_manager import NoteManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
note_manager = NoteManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handle user login."""
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
    """Handle user registration."""
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
    """Display the user dashboard with notes."""
    if 'username' not in session:
        return redirect('/')
    notes = note_manager.get_notes(session['username'])
    return render_template('dashboard.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    """Add a new note for the logged-in user."""
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if title and content:
            note_manager.add_note(session['username'], title, content)
            return redirect('/dashboard')
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET', 'POST'])
def view_note(title):
    """View and edit a specific note."""
    if 'username' not in session:
        return redirect('/')
    notes = note_manager.get_notes(session['username'])
    note_content = next((content for note_title, content in notes if note_title == title), None)
    if request.method == 'POST':
        new_content = request.form['content']
        note_manager.edit_note(session['username'], title, new_content)
        return redirect('/view_note/' + title)
    return render_template('view_note.html', title=title, content=note_content)

@app.route('/delete_note/<title>')
def delete_note(title):
    """Delete a specific note."""
    if 'username' not in session:
        return redirect('/')
    note_manager.delete_note(session['username'], title)
    return redirect('/dashboard')

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    """Search for notes based on a query."""
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        query = request.form['query']
        results = note_manager.search_notes(session['username'], query)
        return render_template('search_note.html', results=results)
    return render_template('search_note.html', results=[])

@app.route('/logout')
def logout():
    """Logout the current user."""
    user_manager.logout()
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8320, debug=False)
