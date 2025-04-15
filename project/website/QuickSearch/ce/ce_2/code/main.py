from flask import Flask, request, redirect, render_template, session
from UserManager import UserManager
from BookManager import BookManager
from ReadingListManager import ReadingListManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
book_manager = BookManager()
reading_list_manager = ReadingListManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
        return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
        return render_template('register.html', error="Username already taken.")
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """Displays the dashboard with available books and search functionality."""
    if 'username' not in session:
        return redirect('/')
    books = book_manager.books
    search_results = []
    if request.method == 'POST':
        query = request.form['search']
        search_results = book_manager.search_books(query)
    return render_template('dashboard.html', books=books, search_results=search_results)

@app.route('/book/<title>', methods=['GET'])
def book_details(title):
    """Displays details of a specific book."""
    book = book_manager.get_book_details(title)
    return render_template('book_details.html', book=book)

@app.route('/reading_list', methods=['GET'])
def reading_list():
    """Displays the user's reading list."""
    if 'username' not in session:
        return redirect('/')
    user_reading_list = reading_list_manager.get_reading_list(session['username'])
    return render_template('reading_list.html', reading_list=user_reading_list)

@app.route('/add_to_reading_list/<title>', methods=['POST'])
def add_to_reading_list(title):
    """Adds a book to the user's reading list."""
    if 'username' in session:
        reading_list_manager.add_to_reading_list(session['username'], title)
    return redirect('/reading_list')

@app.route('/logout', methods=['POST'])
def logout():
    """Logs out the user and redirects to the login page."""
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8325, debug=False)
