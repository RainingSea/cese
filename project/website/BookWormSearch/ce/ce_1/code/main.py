from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class Book:
    def __init__(self, title, author, summary, description):
        self.title = title
        self.author = author
        self.summary = summary
        self.description = description

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file

    def register(self, username, password):
        with open(self.users_file, 'a+') as f:
            f.seek(0)
            for line in f:
                if line.startswith(username + '|'):
                    return False
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2 and parts[0] == username and parts[1] == password:
                    return True
        return False

class BookManager:
    def __init__(self, books_file='books.txt'):
        self.books_file = books_file

    def search(self, query):
        results = []
        with open(self.books_file, 'r') as f:
            for line in f:
                title, author, summary, description = line.strip().split('|')
                if query.lower() in title.lower() or query.lower() in author.lower():
                    results.append(Book(title, author, summary, description))
        return results

    def get_book_details(self, title):
        with open(self.books_file, 'r') as f:
            for line in f:
                book_title, author, summary, description = line.strip().split('|')
                if book_title == title:
                    return Book(book_title, author, summary, description)
        return None

class ReadingListManager:
    def __init__(self, lists_file='reading_lists.txt'):
        self.lists_file = lists_file

    def add_to_list(self, username, book_title):
        lists = self._read_lists()
        if username not in lists:
            lists[username] = []
        if book_title not in lists[username]:
            lists[username].append(book_title)
            self._write_lists(lists)
            return True
        return False

    def get_list(self, username):
        lists = self._read_lists()
        return lists.get(username, [])

    def remove_from_list(self, username, book_title):
        lists = self._read_lists()
        if username in lists and book_title in lists[username]:
            lists[username].remove(book_title)
            self._write_lists(lists)
            return True
        return False

    def _read_lists(self):
        lists = {}
        try:
            with open(self.lists_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 2:
                        username, books = parts
                        lists[username] = books.split(',') if books else []
        except FileNotFoundError:
            pass
        return lists

    def _write_lists(self, lists):
        with open(self.lists_file, 'w') as f:
            for username, books in lists.items():
                f.write(f"{username}|{','.join(books)}\n")

# Initialize managers
user_manager = UserManager()
book_manager = BookManager()
reading_list_manager = ReadingListManager()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('register.html', error="Username already exists")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        query = request.form['query']
        books = book_manager.search(query)
        return render_template('dashboard.html', books=books, username=session['username'])
    
    return render_template('dashboard.html', books=[], username=session['username'])

@app.route('/book/<title>')
def book_details(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    book = book_manager.get_book_details(title)
    if book:
        return render_template('book_details.html', book=book, username=session['username'])
    return redirect(url_for('dashboard'))

@app.route('/add_to_list/<title>')
def add_to_list(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    reading_list_manager.add_to_list(session['username'], title)
    return redirect(url_for('reading_list'))

@app.route('/reading_list')
def reading_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    book_titles = reading_list_manager.get_list(session['username'])
    books = []
    for title in book_titles:
        book = book_manager.get_book_details(title)
        if book:
            books.append(book)
    
    return render_template('reading_list.html', books=books, username=session['username'])

@app.route('/remove_from_list/<title>')
def remove_from_list(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    reading_list_manager.remove_from_list(session['username'], title)
    return redirect(url_for('reading_list'))

if __name__ == '__main__':
    app.run(port=8562, debug=False)
