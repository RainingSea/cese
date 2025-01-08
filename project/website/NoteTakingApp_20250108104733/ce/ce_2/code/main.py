from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from note_manager import NoteManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

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
            return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        notes = note_manager.get_all_notes(session['username'])
        return render_template('dashboard.html', notes=notes)
    return redirect('/')

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' in session:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            note_manager.add_note(session['username'], title, content)
            return redirect('/dashboard')
        return render_template('add_note.html')
    return redirect('/')

@app.route('/view_note/<title>', methods=['GET', 'POST'])
def view_note(title):
    if 'username' in session:
        if request.method == 'POST':
            new_content = request.form['content']
            note_manager.edit_note(session['username'], title, new_content)
            return redirect('/dashboard')
        note = note_manager.get_note(session['username'], title)
        return render_template('view_note.html', note=note)
    return redirect('/')

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if 'username' in session:
        if request.method == 'POST':
            query = request.form['query']
            results = note_manager.search_notes(session['username'], query)
            return render_template('search_note.html', results=results)
        return render_template('search_note.html')
    return redirect('/')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8348, debug=False)
