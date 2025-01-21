from flask import Flask, render_template, request, redirect, session
from user import User
from book import Book
from reading_list import ReadingList
from book_manager import BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users() -> dict:
    """Load users from the users.txt file."""
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users

def load_books() -> list:
    """Load books from the books.txt file."""
    return Book.load_all()

def load_reading_list(username: str) -> list:
    """Load the reading list for a specific user from the reading_list.txt file."""
    reading_list = []
    with open('reading_list.txt', 'r') as file:
        for line in file:
            user, book_title = line.strip().split('|')
            if user == username:
                reading_list.append(book_title)
    return reading_list

users_data = load_users()
books_data = load_books()

@app.route('/')
def login():
    """Render the login page."""
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """Handle user login and render the dashboard with available books."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users_data and users_data[username] == password:
            session['username'] = username
            return render_template('dashboard.html', books=books_data)
    return redirect('/')

@app.route('/book/<title>', methods=['GET'])
def book_details(title: str):
    """Display the details of a specific book."""
    book_manager = BookManager()
    book = book_manager.get_book_details(title)
    if book:
        return render_template('book_details.html', book=book)
    return redirect('/dashboard')

@app.route('/add_to_reading_list', methods=['POST'])
def add_to_reading_list():
    """Add a book to the user's reading list."""
    if 'username' in session:
        book_title = request.form['book_title']
        with open('reading_list.txt', 'a') as file:
            file.write(f"{session['username']}|{book_title}\n")
    return redirect('/dashboard')

@app.route('/remove_from_reading_list/<title>', methods=['GET'])
def remove_from_reading_list(title: str):
    """Remove a book from the user's reading list."""
    if 'username' in session:
        lines = []
        with open('reading_list.txt', 'r') as file:
            lines = file.readlines()
        with open('reading_list.txt', 'w') as file:
            for line in lines:
                if line.strip().split('|')[1] != title or line.strip().split('|')[0] != session['username']:
                    file.write(line)
    return redirect('/reading_list')

@app.route('/reading_list', methods=['GET'])
def reading_list():
    """Display the user's reading list."""
    if 'username' in session:
        user_reading_list = load_reading_list(session['username'])
        return render_template('reading_list.html', reading_list=user_reading_list)
    return redirect('/')

@app.route('/logout', methods=['GET'])
def logout():
    """Log out the user and clear the session."""
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8997, debug=False)
