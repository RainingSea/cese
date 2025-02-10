from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from note_manager import NoteManager

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

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    notes = note_manager.get_notes(username)
    
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
        username = session['username']
        note_manager.add_note(username, title, content)
        return redirect(url_for('dashboard'))
    
    return render_template('add_note.html')

@app.route('/view_note/<int:note_id>')
def view_note(note_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    note = note_manager.get_notes(username)[note_id]
    return render_template('view_note.html', note=note)

@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager.edit_note(username, note_id, title, content)
        return redirect(url_for('dashboard'))
    
    note = note_manager.get_notes(username)[note_id]
    return render_template('add_note.html', title=note['title'], content=note['content'])

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    note_manager.delete_note(username, note_id)
    return redirect(url_for('dashboard'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    results = []
    if request.method == 'POST':
        title = request.form['title']
        results = note_manager.search_notes(username, title)
    
    return render_template('search_note.html', results=results)

if __name__ == '__main__':
    app.run(port=8550, debug=False)
