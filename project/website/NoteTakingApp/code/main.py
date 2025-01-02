from flask import Flask, render_template, request, redirect, url_for, session, flash
import bcrypt
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def load_users(self):
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, hashed_password = line.strip().split(':')
                    users[username] = hashed_password
        return users

    def save_user(self, username: str, password: str):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        with open('users.txt', 'a') as file:
            file.write(f"{username}:{hashed_password}\n")

    def validate_user(self, username: str, password: str) -> bool:
        users = self.load_users()
        if username in users:
            return bcrypt.checkpw(password.encode('utf-8'), users[username].encode('utf-8'))
        return False

class NoteManager:
    def __init__(self, username: str):
        self.username = username

    def add_note(self, title: str, content: str):
        note_id = self.get_next_note_id()
        with open(f'notes_{self.username}.txt', 'a') as file:
            file.write(f"{note_id}:{title}:{content}\n")

    def edit_note(self, note_id: int, title: str, content: str):
        notes = self.get_notes()
        with open(f'notes_{self.username}.txt', 'w') as file:
            for note in notes:
                if note[0] == note_id:
                    file.write(f"{note_id}:{title}:{content}\n")
                else:
                    file.write(f"{note[0]}:{note[1]}:{note[2]}\n")

    def delete_note(self, note_id: int):
        notes = self.get_notes()
        with open(f'notes_{self.username}.txt', 'w') as file:
            for note in notes:
                if note[0] != note_id:
                    file.write(f"{note[0]}:{note[1]}:{note[2]}\n")

    def get_notes(self):
        notes = []
        if os.path.exists(f'notes_{self.username}.txt'):
            with open(f'notes_{self.username}.txt', 'r') as file:
                for line in file:
                    note_id, title, content = line.strip().split(':')
                    notes.append((int(note_id), title, content))
        return notes

    def get_next_note_id(self):
        notes = self.get_notes()
        return max([note[0] for note in notes], default=0) + 1

    def search_notes(self, query: str):
        notes = self.get_notes()
        return [note for note in notes if query.lower() in note[1].lower()]

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager = UserManager()
        user_manager.save_user(username, password)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    note_manager = NoteManager(session['username'])
    notes = note_manager.get_notes()
    return render_template('dashboard.html', notes=notes)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user_manager = UserManager()
    if user_manager.validate_user(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    flash('Invalid username or password', 'danger')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note_manager = NoteManager(session['username'])
        note_manager.add_note(title, content)
        flash('Note added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<int:note_id>', methods=['GET', 'POST'])
def view_note(note_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    note_manager = NoteManager(session['username'])
    
    if request.method == 'POST':
        if 'edit' in request.form:
            title = request.form['title']
            content = request.form['content']
            note_manager.edit_note(note_id, title, content)
            flash('Note updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        elif 'delete' in request.form:
            note_manager.delete_note(note_id)
            flash('Note deleted successfully!', 'success')
            return redirect(url_for('dashboard'))

    notes = note_manager.get_notes()
    note = next((note for note in notes if note[0] == note_id), None)
    
    if note:
        return render_template('view_note.html', note=note)
    else:
        flash('Note not found', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/search_note', methods=['GET', 'POST'])
def search_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    note_manager = NoteManager(session['username'])
    search_results = []
    
    if request.method == 'POST':
        query = request.form['query']
        search_results = note_manager.search_notes(query)
    
    return render_template('search_note.html', results=search_results)

if __name__ == '__main__':
    app.run(port=8177, debug=True)
