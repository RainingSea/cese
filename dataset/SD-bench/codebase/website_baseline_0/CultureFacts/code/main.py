from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from culture_manager import CultureManager
from bookmark_manager import BookmarkManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
culture_manager = CultureManager('cultures.txt')
bookmark_manager = BookmarkManager('bookmarks.txt')

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
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        return "Registration failed. Username may already exist."
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Renders the dashboard with available cultures."""
    cultures = culture_manager.cultures
    return render_template('dashboard.html', cultures=cultures)

@app.route('/culture/<culture_name>')
def culture_details(culture_name):
    """Renders details for a specific culture."""
    details = culture_manager.get_culture_details(culture_name)
    return render_template('culture_details.html', details=details)

@app.route('/bookmarks')
def bookmarks():
    """Renders the bookmarks page for the logged-in user."""
    username = session.get('username')
    if username is None:
        return redirect(url_for('login'))
    user_bookmarks = bookmark_manager.get_bookmarks(username)
    return render_template('bookmarks.html', bookmarks=user_bookmarks)

@app.route('/login', methods=['POST'])
def do_login():
    """Handles user login."""
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Login failed. Check your username and password."

@app.route('/logout')
def logout():
    """Logs out the user."""
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8529, debug=False)
