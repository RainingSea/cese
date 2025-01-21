from flask import Flask, render_template, request, redirect, url_for, session
from user import User, UserManager
from journal import JournalEntry, JournalManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
journal_manager = JournalManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="Username already exists.")
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Displays the dashboard with journal entries."""
    if 'username' not in session:
        return redirect(url_for('login'))
    entries = journal_manager.load_entries()
    return render_template('dashboard.html', entries=entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    """Handles creation of a new journal entry."""
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        journal_manager.create_entry(title, content)
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html')

@app.route('/logout')
def logout():
    """Logs out the user."""
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    user_manager.load_users()
    journal_manager.load_entries()
    app.run(port=8937, debug=False)
