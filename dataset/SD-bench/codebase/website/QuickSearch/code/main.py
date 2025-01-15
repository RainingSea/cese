from flask import Flask, render_template, request, redirect, session, url_for
from bcrypt import hashpw, gensalt, checkpw
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self):
        self.users = self.load_users('users.txt')

    def load_users(self, file_path: str) -> dict:
        """Load users from a file."""
        users = {}
        with open(file_path, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
        return users

    def register(self, username: str, password: str) -> bool:
        """Register a new user."""
        if username not in self.users:
            hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
            self.users[username] = hashed_password
            with open('users.txt', 'a') as file:
                file.write(f"{username}|{hashed_password}\n")
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        """Login a user."""
        stored_password = self.users.get(username)
        if stored_password and checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            session['username'] = username
            return True
        return False

    def logout(self) -> None:
        """Logout the user by clearing the session."""
        session.pop('username', None)

class Book:
    def __init__(self, title: str, author: str, summary: str, cover_image: str):
        self.title = title
        self.author = author
        self.summary = summary
        self.cover_image = cover_image

    @staticmethod
    def load_books() -> list:
        """Load books from a file."""
        books = []
        with open('books.txt', 'r') as file:
            for line in file:
                title, author, summary, cover_image = line.strip().split('|')
                books.append(Book(title, author, summary, cover_image))
        return books

class ReadingList:
    def __init__(self, user: User):
        self.user = user
        self.books = self.load_reading_list()

    def add_book(self, book: Book) -> None:
        """Add a book to the reading list."""
        if book.title not in [b.title for b in self.books]:
            self.books.append(book)
            self.save_reading_list()

    def remove_book(self, book: Book) -> None:
        """Remove a book from the reading list."""
        self.books = [b for b in self.books if b.title != book.title]
        self.save_reading_list()

    def load_reading_list(self) -> list:
        """Load the reading list from a file."""
        reading_list = []
        if os.path.exists('reading_list.txt'):
            with open('reading_list.txt', 'r') as file:
                for line in file:
                    username, book_title = line.strip().split('|')
                    if username == self.user.username:
                        reading_list.append(Book(book_title, "", "", ""))
        return reading_list

    def save_reading_list(self) -> None:
        """Save the reading list to a file."""
        with open('reading_list.txt', 'w') as file:
            for book in self.books:
                file.write(f"{self.user.username}|{book.title}\n")

class QuickSearchApp:
    def __init__(self):
        self.users = User()
        self.books = Book.load_books()
        self.reading_lists = {}

    def register(self, username: str, password: str) -> bool:
        """Register a new user."""
        return self.users.register(username, password)

    def login(self, username: str, password: str) -> User:
        """Login a user and return the user object."""
        if self.users.login(username, password):
            return self.users.load_users('users.txt')[username]
        return None

    def search_books(self, query: str) -> list:
        """Search for books by title."""
        results = [book for book in self.books if query.lower() in book.title.lower()]
        return results if results else "No books found."

    def get_book_details(self, title: str) -> Book:
        """Get details of a specific book."""
        for book in self.books:
            if book.title == title:
                return book
        return None

    def add_to_reading_list(self, user: User, book: Book) -> None:
        """Add a book to the user's reading list."""
        if user.username not in self.reading_lists:
            self.reading_lists[user.username] = ReadingList(user)
        self.reading_lists[user.username].add_book(book)

    def get_reading_list(self, user: User) -> ReadingList:
        """Get the user's reading list."""
        if user.username not in self.reading_lists:
            self.reading_lists[user.username] = ReadingList(user)
        return self.reading_lists[user.username]

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app.quick_search_app.login(username, password):
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app.quick_search_app.register(username, password):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="Username already exists.")
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Display the dashboard with available books."""
    if 'username' not in session:
        return redirect(url_for('login'))
    books = app.quick_search_app.books
    return render_template('dashboard.html', books=books)

@app.route('/book/<title>')
def book_details(title):
    """Display details of a specific book."""
    book = app.quick_search_app.get_book_details(title)
    return render_template('book_details.html', book=book)

@app.route('/reading_list')
def reading_list():
    """Display the user's reading list."""
    if 'username' not in session:
        return redirect(url_for('login'))
    user = session['username']
    reading_list = app.quick_search_app.get_reading_list(app.quick_search_app.users.load_users('users.txt')[user])
    return render_template('reading_list.html', reading_list=reading_list.books)

@app.route('/logout')
def logout():
    """Handle user logout."""
    app.quick_search_app.users.logout()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.quick_search_app = QuickSearchApp()
    app.run(port=8685, debug=False)
