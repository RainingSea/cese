from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from NoteManager import NoteManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
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

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        notes = note_manager.get_notes(session['username'])
        return render_template('dashboard.html', notes=notes)
    return redirect(url_for('login'))

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' in session:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            note_manager.add_note(session['username'], title, content)
            return redirect(url_for('dashboard'))
        return render_template('add_note.html')
    return redirect(url_for('login'))

@app.route('/view_note/<title>')
def view_note(title):
    if 'username' in session:
        note = note_manager.get_note(session['username'], title)
        return render_template('view_note.html', note=note)
    return redirect(url_for('login'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if 'username' in session:
        if request.method == 'POST':
            query = request.form['query']
            results = note_manager.search_notes(session['username'], query)
            return render_template('search_note.html', results=results)
        return render_template('search_note.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def login_user():
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
    app.run(port=8548, debug=False)
