from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from BookManager import BookManager
from ReadingListManager import ReadingListManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
book_manager = BookManager()
reading_list_manager = ReadingListManager()

@app.route('/')
def login():
    """Render the login page."""
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """Render the dashboard and handle book search."""
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        query = request.form['query']
        results = book_manager.search_books(query)
        return render_template('dashboard.html', results=results)
    return render_template('dashboard.html')

@app.route('/login', methods=['POST'])
def do_login():
    """Handle user login."""
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    """Logout a user."""
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/book/<title>')
def book_details(title):
    """Render the details of a specific book."""
    details = book_manager.get_book_details(title)
    return render_template('book_details.html', details=details)

@app.route('/add_to_reading_list/<book_title>')
def add_to_reading_list(book_title):
    """Add a book to the user's reading list."""
    username = session.get('username')
    if username:
        reading_list_manager.add_to_reading_list(username, book_title)
    return redirect(url_for('dashboard'))

@app.route('/reading_list')
def reading_list():
    """Render the user's reading list."""
    username = session.get('username')
    if username is None:
        return redirect(url_for('login'))
    
    books = reading_list_manager.get_reading_list(username)
    return render_template('reading_list.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)