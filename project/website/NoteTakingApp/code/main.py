from flask import Flask, render_template, request, redirect, url_for, session, flash
from auth_manager import AuthManager
from note_manager import NoteManager
from search_manager import SearchManager

app = Flask(__name__)
app.secret_key = 'secret_key'

auth_manager = AuthManager()
note_manager = NoteManager()
search_manager = SearchManager(note_manager)

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if auth_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if auth_manager.register(username, password, confirm_password):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username may exist or passwords do not match.', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    notes = note_manager.get_notes(username)
    return render_template('dashboard.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        username = session['username']
        
        if note_manager.add_note(username, title, content):
            flash('Note added successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Title and content cannot be empty', 'error')
            return render_template('add_note.html')
    
    return render_template('add_note.html')

@app.route('/view_note/<note_id>', methods=['GET', 'POST'])
def view_note(note_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    note = note_manager.get_note(username, note_id)
    
    if not note:
        flash('Note not found', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        if 'delete' in request.form:
            note_manager.delete_note(username, note_id)
            flash('Note deleted successfully', 'success')
            return redirect(url_for('dashboard'))
        else:
            new_title = request.form['title']
            content = request.form['content']
            note_manager.update_note(username, note_id, new_title, content)
            flash('Note updated successfully', 'success')
            return redirect(url_for('dashboard'))
    
    return render_template('view_note.html', note={'id': note_id, **note})

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    if request.method == 'POST':
        query = request.form['query']
        results = search_manager.search_by_title(username, query)
        return render_template('search.html', results=results, query=query)
    
    return render_template('search.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8097, debug=False)
