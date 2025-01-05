from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from note import Note
from file_manager import FileManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in a production environment

file_manager = FileManager()
users_data = file_manager.read_users()
notes_data = file_manager.read_notes()

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
    return render_template('dashboard.html', notes=notes_data)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note = Note(title, content)
        if note.create(title, content):
            notes_data.append((title, content))
            file_manager.write_notes(notes_data)
            return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET'])
def view_note(title):
    for note in notes_data:
        if note[0] == title:
            return render_template('view_note.html', title=note[0], content=note[1])
    return redirect(url_for('dashboard'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if request.method == 'POST':
        title = request.form['title']
        results = []
        for note in notes_data:
            if title in note[0]:
                results.append(note)
        return render_template('search_note.html', results=results)
    return render_template('search_note.html', results=[])

if __name__ == '__main__':
    app.run(port=8029, debug=False)
