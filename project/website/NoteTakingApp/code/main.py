from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from note import Note
from file_manager import FileManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

file_manager = FileManager()
users = file_manager.read_users()
notes = file_manager.read_notes()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        user_notes = [note for note in notes if note['username'] == session['username']]
        return render_template('dashboard.html', notes=user_notes)
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    if user.login(username, password):
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
        note = Note(title, content)
        note.create(title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>')
def view_note(title):
    note = next((note for note in notes if note['title'] == title), None)
    return render_template('view_note.html', note=note)

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if request.method == 'POST':
        title = request.form['title']
        search_results = [note for note in notes if title in note['title']]
        return render_template('search_note.html', results=search_results)
    return render_template('search_note.html')

if __name__ == '__main__':
    app.run(port=8033, debug=False)
