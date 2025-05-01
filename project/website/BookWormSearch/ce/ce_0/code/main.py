from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key'

class Book:
    def __init__(self, title, author, description):
        self.title = title
        self.author = author
        self.description = description

class BookManager:
    def __init__(self, books_file='books.txt'):
        self.books_file = books_file

    def search_books(self, query):
        books = []
        with open(self.books_file, 'r') as f:
            for line in f:
                title, author, description = line.strip().split('|')
                if query.lower() in title.lower() or query.lower() in author.lower():
                    books.append(Book(title, author, description))
        return books

    def get_book_details(self, title):
        with open(self.books_file, 'r') as f:
            for line in f:
                book_title, author, description = line.strip().split('|')
                if book_title == title:
                    return Book(book_title, author, description)
        return None

class ReadingListManager:
    def __init__(self, lists_file='reading_lists.txt'):
        self.lists_file = lists_file

    def add_to_list(self, username, book_title):
        lists = self._read_lists()
        if username in lists:
            if book_title not in lists[username]:
                lists[username].append(book_title)
        else:
            lists[username] = [book_title]
        self._write_lists(lists)

    def get_list(self, username):
        lists = self._read_lists()
        return lists.get(username, [])

    def remove_from_list(self, username, book_title):
        lists = self._read_lists()
        if username in lists and book_title in lists[username]:
            lists[username].remove(book_title)
            self._write_lists(lists)

    def _read_lists(self):
        lists = {}
        try:
            with open(self.lists_file, 'r') as f:
                for line in f:
                    username, books_str = line.strip().split('|')
                    lists[username] = books_str.split(',') if books_str else []
        except FileNotFoundError:
            pass
        return lists

    def _write_lists(self, lists):
        with open(self.lists_file, 'w') as f:
            for username, books in lists.items():
                f.write(f"{username}|{','.join(books)}\n")

class BookWormApp:
    def __init__(self):
        self.current_user = None
        self.book_manager = BookManager()
        self.reading_list_manager = ReadingListManager()

    def register(self, username, password):
        with open('users.txt', 'a+') as f:
            f.seek(0)
            for line in f:
                existing_username, _ = line.strip().split('|')
                if existing_username == username:
                    return False
            f.write(f"{username}|{generate_password_hash(password)}\n")
        return True

    def login(self, username, password):
        with open('users.txt', 'r') as f:
            for line in f:
                existing_username, existing_password = line.strip().split('|')
                if existing_username == username and check_password_hash(existing_password, password):
                    self.current_user = username
                    return True
        return False

    def logout(self):
        self.current_user = None

app_instance = BookWormApp()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app_instance.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app_instance.register(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        query = request.form['query']
        books = app_instance.book_manager.search_books(query)
        return render_template('dashboard.html', books=books, username=session['username'])
    
    return render_template('dashboard.html', books=[], username=session['username'])

@app.route('/book/<title>')
def book_details(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    book = app_instance.book_manager.get_book_details(title)
    if not book:
        return redirect(url_for('dashboard'))
    
    return render_template('book_details.html', book=book, username=session['username'])

@app.route('/add_to_list/<title>')
def add_to_list(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    app_instance.reading_list_manager.add_to_list(session['username'], title)
    return redirect(url_for('reading_list'))

@app.route('/reading_list')
def reading_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    book_titles = app_instance.reading_list_manager.get_list(session['username'])
    books = []
    for title in book_titles:
        book = app_instance.book_manager.get_book_details(title)
        if book:
            books.append(book)
    
    return render_template('reading_list.html', books=books, username=session['username'])

@app.route('/remove_from_list/<title>')
def remove_from_list(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    app_instance.reading_list_manager.remove_from_list(session['username'], title)
    return redirect(url_for('reading_list'))

@app.route('/logout')
def logout():
    app_instance.logout()
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8561, debug=False)
