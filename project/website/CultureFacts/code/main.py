from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.utils import secure_filename
from user import User
from culture import Culture
from bookmark import Bookmark
from culture_facts_app import CultureFactsApp

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the application with file paths
app_instance = CultureFactsApp('users.txt', 'cultures.txt', 'bookmarks.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = app_instance.login(username, password)
        if user:
            session['username'] = username
            return redirect('/dashboard')
        else:
            flash('Login failed. Please check your credentials.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app_instance.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect('/')
        else:
            flash('Registration failed. Username may already exist.')
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Displays the culture dashboard."""
    if 'username' in session:
        cultures = app_instance.search_cultures('')
        return render_template('dashboard.html', cultures=cultures)
    return redirect('/')

@app.route('/culture/<name>', methods=['GET'])
def culture_details(name):
    """Displays details of a specific culture."""
    culture = app_instance.get_culture_details(name)
    if culture == "Culture not found.":
        flash(culture)
        return redirect('/dashboard')
    return render_template('culture_details.html', culture=culture)

@app.route('/bookmarks', methods=['GET'])
def bookmarks():
    """Displays the user's bookmarks."""
    user = session.get('username')
    if user:
        bookmarks = app_instance.get_bookmarks(User(user, ''))
        return render_template('bookmarks.html', bookmarks=bookmarks)
    return redirect('/')

@app.route('/bookmark/<culture_name>', methods=['POST'])
def bookmark(culture_name):
    """Bookmarks a culture for the logged-in user."""
    user = session.get('username')
    if user:
        app_instance.bookmark_culture(User(user, ''), culture_name)
        flash(f'Culture "{culture_name}" bookmarked successfully!')
        return redirect('/bookmarks')
    return redirect('/')

@app.route('/remove_bookmark/<culture_name>', methods=['POST'])
def remove_bookmark(culture_name):
    """Removes a bookmark for the logged-in user."""
    user = session.get('username')
    if user:
        app_instance.remove_bookmark(User(user, ''), culture_name)
        flash(f'Bookmark for "{culture_name}" removed successfully!')
        return redirect('/bookmarks')
    return redirect('/')

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Handles culture search functionality."""
    if request.method == 'POST':
        keyword = request.form['keyword']
        cultures = app_instance.search_cultures(keyword)
        return render_template('dashboard.html', cultures=cultures)
    return redirect('/dashboard')

@app.route('/logout', methods=['POST'])
def logout():
    """Logs out the user and redirects to the login page."""
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect('/')

if __name__ == '__main__':
    app.run(port=9021, debug=False)
