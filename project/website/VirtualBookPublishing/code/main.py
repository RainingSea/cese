from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self, filename='users.txt'):
        self.filename = filename
        self.users = self.load_users()

    def register(self, username: str, password: str) -> bool:
        """Register a new user if the username does not already exist."""
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.filename, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        """Check if the username and password match."""
        return self.users.get(username) == password

    def load_users(self) -> dict:
        """Load users from the specified file."""
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename, 'r') as f:
            return dict(line.strip().split('|') for line in f)

class BookManager:
    def __init__(self, filename='books.txt'):
        self.filename = filename
        self.books = self.load_books()

    def create_book(self, title: str, author: str, content: str) -> bool:
        """Create a new book if the title does not already exist."""
        if title in self.books:
            return False
        self.books[title] = {'author': author, 'content': content}
        with open(self.filename, 'a') as f:
            f.write(f"{title}|{author}|{content}\n")
        return True

    def get_books(self) -> list:
        """Return a list of book titles."""
        return list(self.books.keys())

    def get_book_details(self, title: str) -> dict:
        """Return the details of a specific book."""
        return self.books.get(title)

    def load_books(self) -> dict:
        """Load books from the specified file."""
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename, 'r') as f:
            return {line.split('|')[0]: {'author': line.split('|')[1], 'content': line.split('|')[2]} for line in f}

user_manager = UserManager()
book_manager = BookManager()

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
        else:
            return "Username already exists!"
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """Render the dashboard after successful login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return render_template('dashboard.html', username=username)
        else:
            return "Invalid credentials!"
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/create_book', methods=['GET', 'POST'])
def create_book():
    """Handle book creation."""
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        if book_manager.create_book(title, author, content):
            return redirect(url_for('my_books'))
        else:
            return "Book with this title already exists!"
    return render_template('create_book.html')

@app.route('/my_books')
def my_books():
    """Render the list of books created by the user."""
    books = book_manager.get_books()
    return render_template('my_books.html', books=books)

@app.route('/book_details/<title>')
def book_details(title):
    """Render the details of a specific book."""
    book = book_manager.get_book_details(title)
    if book:
        return render_template('book_details.html', title=title, author=book['author'], content=book['content'])
    return "Book not found!"

@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=8457, debug=False)
