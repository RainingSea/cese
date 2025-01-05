from flask import Flask, render_template, request, redirect, session, url_for
from user_manager import UserManager
from note_manager import NoteManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
note_manager = None

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

@app.route('/dashboard')
def dashboard():
    global note_manager
    if 'username' in session:
        note_manager = NoteManager(session['username'])
        notes = note_manager.get_all_notes()
        return render_template('dashboard.html', notes=notes)
    return redirect(url_for('login'))

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
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager.add_note(title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET'])
def view_note(title):
    note = note_manager.get_all_notes()
    for n in note:
        if n.split('|')[0] == title:
            return render_template('view_note.html', note=n)
    return redirect(url_for('dashboard'))

@app.route('/delete_note/<title>', methods=['POST'])
def delete_note(title):
    note_manager.delete_note(title)
    return redirect(url_for('dashboard'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if request.method == 'POST':
        query = request.form['query']
        results = note_manager.search_notes(query)
        return render_template('search_note.html', results=results)
    return render_template('search_note.html', results=[])

if __name__ == '__main__':
    app.run(port=8098, debug=False)
