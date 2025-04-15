from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from note_manager import NoteManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

user_manager = UserManager('users.txt')
note_manager = NoteManager('notes.txt', 'metadata.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
        else:
            return render_template('register.html', error="Username already exists.")
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    notes = note_manager.get_notes()
    return render_template('dashboard.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager.add_note(title, content)
        return redirect('/dashboard')
    return render_template('add_note.html')

@app.route('/view_note/<title>', methods=['GET', 'POST'])
def view_note(title):
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        new_content = request.form['content']
        note_manager.edit_note(title, new_content)
        return redirect('/dashboard')
    note = note_manager.get_note(title)
    return render_template('view_note.html', title=title, content=note)

@app.route('/delete_note/<title>')
def delete_note(title):
    if 'username' not in session:
        return redirect('/')
    note_manager.delete_note(title)
    return redirect('/dashboard')

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        query = request.form['query']
        results = note_manager.search_notes(query)
        return render_template('search_note.html', results=results)
    return render_template('search_note.html', results=[])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8315, debug=False)
