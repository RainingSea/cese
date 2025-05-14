from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret_key'

def load_users():
    users = {}
    try:
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split(':')
                users[username] = password
    except FileNotFoundError:
        pass
    return users

def save_user(username, password):
    with open('users.txt', 'a') as f:
        f.write(f"{username}:{password}\n")

def load_notes(username):
    notes = []
    try:
        with open('notes.txt', 'r') as f:
            for line in f:
                user, title, content = line.strip().split(':', 2)
                if user == username:
                    notes.append({'title': title, 'content': content})
    except FileNotFoundError:
        pass
    return notes

def save_note(username, title, content):
    with open('notes.txt', 'a') as f:
        f.write(f"{username}:{title}:{content}\n")

def update_note(username, old_title, new_title, new_content):
    notes = []
    updated = False
    try:
        with open('notes.txt', 'r') as f:
            for line in f:
                user, title, content = line.strip().split(':', 2)
                if user == username and title == old_title:
                    notes.append(f"{username}:{new_title}:{new_content}\n")
                    updated = True
                else:
                    notes.append(line)
        
        if updated:
            with open('notes.txt', 'w') as f:
                f.writelines(notes)
        return updated
    except FileNotFoundError:
        return False

def delete_note(username, title):
    notes = []
    deleted = False
    try:
        with open('notes.txt', 'r') as f:
            for line in f:
                user, t, content = line.strip().split(':', 2)
                if not (user == username and t == title):
                    notes.append(line)
                else:
                    deleted = True
        
        if deleted:
            with open('notes.txt', 'w') as f:
                f.writelines(notes)
        return deleted
    except FileNotFoundError:
        return False

def search_notes(username, query):
    notes = []
    try:
        with open('notes.txt', 'r') as f:
            for line in f:
                user, title, content = line.strip().split(':', 2)
                if user == username and query.lower() in title.lower():
                    notes.append({'title': title, 'content': content})
    except FileNotFoundError:
        pass
    return notes

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        
        if password != confirm:
            return render_template('register.html', error='Passwords do not match')
        
        users = load_users()
        if username in users:
            return render_template('register.html', error='Username already exists')
        
        save_user(username, password)
        session['username'] = username
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    notes = load_notes(session['username'])
    return render_template('dashboard.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        save_note(session['username'], title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<title>')
def view_note(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    notes = load_notes(session['username'])
    for note in notes:
        if note['title'] == title:
            return render_template('view_note.html', note=note)
    return redirect(url_for('dashboard'))

@app.route('/edit_note/<old_title>', methods=['GET', 'POST'])
def edit_note(old_title):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        update_note(session['username'], old_title, new_title, new_content)
        return redirect(url_for('dashboard'))
    
    notes = load_notes(session['username'])
    for note in notes:
        if note['title'] == old_title:
            return render_template('edit_note.html', note=note)
    return redirect(url_for('dashboard'))

@app.route('/delete_note/<title>')
def delete_note_route(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    delete_note(session['username'], title)
    return redirect(url_for('dashboard'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        query = request.form['query']
        results = search_notes(session['username'], query)
        return render_template('search.html', results=results, query=query)
    return render_template('search.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8096, debug=False)
