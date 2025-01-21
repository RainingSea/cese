from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from note_manager import NoteManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
note_manager = NoteManager('notes.txt')

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

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager.add_note(session['username'], title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET'])
def view_note(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    notes = note_manager.get_notes(session['username'])
    content = note_manager.notes.get(title)
    return render_template('view_note.html', title=title, content=content)

@app.route('/edit_note/<title>', methods=['GET', 'POST'])
def edit_note(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_content = request.form['content']
        note_manager.edit_note(session['username'], title, new_content)
        return redirect(url_for('dashboard'))
    content = note_manager.notes.get(title)
    return render_template('add_note.html', title=title, content=content)

@app.route('/delete_note/<title>', methods=['GET'])
def delete_note(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    note_manager.delete_note(session['username'], title)
    return redirect(url_for('dashboard'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        results = note_manager.search_notes(session['username'], title)
        return render_template('search_note.html', results=results)
    return render_template('search_note.html', results=[])

if __name__ == '__main__':
    app.run(port=8957, debug=False)
