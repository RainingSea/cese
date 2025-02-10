from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from note import Note

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize User and Note classes
user_manager = User()
note_manager = Note()

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

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    notes = note_manager.search_notes(username, "")
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
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        username = session['username']
        note_manager.create_note(username, title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET'])
def view_note(title):
    username = session['username']
    note = note_manager.search_notes(username, title)
    return render_template('view_note.html', note=note[0] if note else None)

@app.route('/edit_note/<title>', methods=['GET', 'POST'])
def edit_note(title):
    if request.method == 'POST':
        content = request.form['content']
        note_manager.edit_note(title, content)
        return redirect(url_for('dashboard'))
    username = session['username']
    note = note_manager.search_notes(username, title)
    return render_template('add_note.html', title=title, content=note[0].content if note else "")

@app.route('/delete_note/<title>', methods=['GET'])
def delete_note(title):
    username = session['username']
    note_manager.delete_note(title)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=8549, debug=False)
