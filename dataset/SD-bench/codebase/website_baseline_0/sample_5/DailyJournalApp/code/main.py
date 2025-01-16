from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from journal_manager import JournalManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
user_manager = UserManager('users.txt')
journal_manager = JournalManager('journal_entries.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username  # Store username in session
            return redirect(url_for('dashboard'))
        return "Login failed. Please check your credentials."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        return "Registration failed. Username may already exist."
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not authenticated
    entries = journal_manager.get_entries()
    return render_template('dashboard.html', entries=entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not authenticated
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        journal_manager.create_entry(title, content)
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8447, debug=False)
