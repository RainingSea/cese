from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from note_manager import NoteManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'
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

@app.route('/dashboard', methods=['GET'])
def dashboard():
    username = session.get('username')
    global note_manager
    note_manager = NoteManager(f'notes_{username}.txt')
    notes = note_manager.get_notes()
    return render_template('dashboard.html', notes=notes)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
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
    notes = note_manager.get_notes()
    note = next((note for note in notes if note['title'] == title), None)
    return render_template('view_note.html', note=note)

@app.route('/edit_note/<title>', methods=['POST'])
def edit_note(title):
    new_content = request.form['content']
    note_manager.edit_note(title, new_content)
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
    app.run(port=8551, debug=False)
