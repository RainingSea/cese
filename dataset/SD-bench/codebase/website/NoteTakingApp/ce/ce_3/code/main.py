from flask import Flask, render_template, request, redirect, url_for, session
from User import User
from Note import Note

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    user = User()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials!"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    user = User()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user.register(username, password):
            return redirect(url_for('login'))
        else:
            return "User already exists!"
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    note = Note(username)
    notes = note.file_manager.load_note_data(username)
    return render_template('dashboard.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    username = session.get('username')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note = Note(username)
        note.create_note(title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET', 'POST'])
def view_note(title):
    username = session.get('username')
    note = Note(username)
    notes = note.file_manager.load_note_data(username)
    selected_note = next((n for n in notes if n['title'] == title), None)
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        note.edit_note(selected_note['title'], new_title, new_content)
        return redirect(url_for('dashboard'))
    return render_template('view_note.html', note=selected_note)

@app.route('/delete_note/<title>')
def delete_note(title):
    username = session.get('username')
    note = Note(username)
    note.delete_note(title)
    return redirect(url_for('dashboard'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    username = session.get('username')
    notes = []
    if request.method == 'POST':
        search_term = request.form['search_term']
        note = Note(username)
        all_notes = note.file_manager.load_note_data(username)
        notes = [n for n in all_notes if search_term in n['title'] or search_term in n['content']]
    return render_template('search_note.html', notes=notes)

if __name__ == '__main__':
    app.run(port=8462, debug=False)
