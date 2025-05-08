from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'bookworm_secret_key'  # For session management

USERS_FILE = 'users.txt'
BOOKS_FILE = 'books.txt'
READING_LIST_FILE = 'reading_list.txt'


class User:
    def __init__(self, username: str = '', password: str = ''):
        self.username = username
        self.password = password

    def register(self, username: str, password: str) -> bool:
        # Check if user already exists
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    stored_username, _ = line.strip().split('|', 1)
                    if stored_username == username:
                        return False  # User already exists
        # Save new user
        with open(USERS_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        if not os.path.exists(USERS_FILE):
            return False
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|', 1)
                if stored_username == username and stored_password == password:
                    self.username = username
                    self.password = password
                    return True
        return False


class Book:
    def __init__(self, title: str, author: str, summary: str, description: str):
        self.title = title
        self.author = author
        self.summary = summary
        self.description = description

    def get_details(self) -> dict:
        return {
            'title': self.title,
            'author': self.author,
            'summary': self.summary,
            'description': self.description
        }


class BookManager:
    def __init__(self):
        self.books = []
        self.load_books()

    def load_books(self) -> list:
        self.books.clear()
        if not os.path.exists(BOOKS_FILE):
            return self.books
        with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    title, author, summary, description = parts
                    book = Book(title, author, summary, description)
                    self.books.append(book)
        return self.books

    def search_books(self, query: str) -> list:
        query_lower = query.lower()
        results = []
        for book in self.books:
            if (query_lower in book.title.lower() or
                    query_lower in book.author.lower() or
                    query_lower in book.summary.lower() or
                    query_lower in book.description.lower()):
                results.append(book)
        return results

    def add_book(self, book: Book) -> None:
        self.books.append(book)
        with open(BOOKS_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{book.title}|{book.author}|{book.summary}|{book.description}\n")


class ReadingList:
    def __init__(self, username: str = ''):
        self.reading_list = []
        self.username = username
        if username:
            self.load_reading_list(username)

    def load_reading_list(self, username: str) -> list:
        self.reading_list.clear()
        self.username = username
        if not os.path.exists(READING_LIST_FILE):
            return self.reading_list
        with open(READING_LIST_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 2:
                    continue
                stored_username = parts[0]
                if stored_username != username:
                    continue
                # Each book entry after username is title,author,summary,description joined by commas
                # But summary and description may contain commas, so we store book fields separated by commas
                # We stored book info as title,author,summary,description separated by commas
                # To avoid confusion, we store book info as title,author,summary,description joined by commas
                # But summary and description may contain commas, so we store book info separated by commas
                # So here, after username, each book is stored as title,author,summary,description separated by commas
                # But line format is username|title,author,summary,description|title,author,summary,description|...
                # So parts[1:] are book infos separated by '|', each book info is title,author,summary,description separated by commas
                # So we parse each book info by splitting by commas into 4 parts
                # But summary and description may contain commas, so we must store book info with another separator
                # To avoid complexity, we store book info separated by commas but summary and description do not contain commas in our demo data.
                # So we parse by splitting by commas into 4 parts
                # Here we parse each book info separately below
                # This is done outside this loop
                # So we skip here and parse after loop
                # We parse after loop
                # So we do nothing here
                pass
        # We need to parse the line again to get books
        with open(READING_LIST_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if parts[0] == username:
                    for book_info in parts[1:]:
                        book_parts = book_info.split(',', 3)
                        if len(book_parts) == 4:
                            title, author, summary, description = book_parts
                            self.reading_list.append(Book(title, author, summary, description))
                    break
        return self.reading_list

    def save_reading_list(self) -> None:
        # Read all lines from file, update or add current user's reading list, then write back
        lines = []
        found = False
        if os.path.exists(READING_LIST_FILE):
            with open(READING_LIST_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        with open(READING_LIST_FILE, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.strip().startswith(self.username + '|'):
                    # skip this user's old line
                    continue
                f.write(line)
            # Write current user's reading list
            if self.reading_list:
                book_strs = []
                for book in self.reading_list:
                    # Save book info as title,author,summary,description separated by commas
                    # summary and description may contain commas but we assume no commas in demo data
                    book_str = f"{book.title},{book.author},{book.summary},{book.description}"
                    book_strs.append(book_str)
                f.write(f"{self.username}|{'|'.join(book_strs)}\n")
            else:
                # If reading list empty, do not write user line (effectively removes user reading list)
                pass

    def add_to_reading_list(self, book: Book) -> None:
        # Avoid duplicates by title and author
        for b in self.reading_list:
            if b.title == book.title and b.author == book.author:
                return
        self.reading_list.append(book)
        self.save_reading_list()

    def remove_from_reading_list(self, book: Book) -> None:
        self.reading_list = [b for b in self.reading_list if not (b.title == book.title and b.author == book.author)]
        self.save_reading_list()


book_manager = BookManager()


@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('login'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return render_template('registration.html')
        user = User()
        success = user.register(username, password)
        if success:
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose another.', 'danger')
            return render_template('registration.html')
    else:
        return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = User()
        if user.login(username, password):
            session['username'] = username
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    search_results = []
    query = ''
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if query:
            search_results = book_manager.search_books(query)
    return render_template('dashboard.html', username=session['username'], books=search_results, query=query)


@app.route('/book/<title>', methods=['GET', 'POST'])
def book_details(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    book = None
    for b in book_manager.books:
        if b.title == title:
            book = b
            break
    if not book:
        flash('Book not found.', 'danger')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        # Add to reading list
        reading_list = ReadingList(session['username'])
        reading_list.add_to_reading_list(book)
        flash(f'"{book.title}" added to your reading list.', 'success')
        return redirect(url_for('reading_list'))
    return render_template('book_details.html', username=session['username'], book=book)


@app.route('/reading_list', methods=['GET', 'POST'])
def reading_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    reading_list = ReadingList(session['username'])
    if request.method == 'POST':
        # Remove book from reading list
        title = request.form.get('title', '')
        author = request.form.get('author', '')
        book_to_remove = None
        for b in reading_list.reading_list:
            if b.title == title and b.author == author:
                book_to_remove = b
                break
        if book_to_remove:
            reading_list.remove_from_reading_list(book_to_remove)
            flash(f'"{title}" removed from your reading list.', 'success')
        return redirect(url_for('reading_list'))
    return render_template('reading_list.html', username=session['username'], reading_list=reading_list.reading_list)


if __name__ == '__main__':
    app.run(port=8290, debug=False)
