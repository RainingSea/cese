from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from note import Note

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def login():
    """Renders the login page."""
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register(username, password):
            return redirect(url_for('login'))
        return "Registration failed. Username already exists."
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """Renders the user dashboard."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    note = Note(username, "", "")

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note.create_note(username, title, content)

    notes = note.get_notes(username)
    return render_template('dashboard.html', notes=notes)

@app.route('/login', methods=['POST'])
def do_login():
    """Handles user login."""
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    if user.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Login failed. Invalid credentials."

@app.route('/logout')
def logout():
    """Logs out the user."""
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8308, debug=False)
