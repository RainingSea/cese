import json
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'replace_with_a_secure_random_key_for_production'

USERS_FILE = 'users.txt'
BOOKS_FILE = 'books.txt'
READING_LIST_FILE = 'reading_lists.txt'


class UserManager:
    def register(self, username: str, password: str) -> bool:
        if self.user_exists(username):
            return False
        user = {"username": username, "password": password}
        self._save_user(user)
        return True

    def login(self, username: str, password: str) -> bool:
        users = self._load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

    def user_exists(self, username: str) -> bool:
        users = self._load_users()
        for user in users:
            if user['username'] == username:
                return True
        return False

    def _load_users(self) -> list:
        users = []
        if not os.path.exists(USERS_FILE):
            return users
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        user = json.loads(line)
                        users.append(user)
                    except json.JSONDecodeError:
                        continue
        return users

    def _save_user(self, user: dict) -> None:
        with open(USERS_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(user, ensure_ascii=False) + '\n')


class BookManager:
    def search_books(self, query: str) -> list:
        query_lower = query.lower()
        books = self._load_books()
        results = []
        for book in books:
            if (query_lower in book['title'].lower() or
                query_lower in book['author'].lower() or
                query_lower in book['summary'].lower()):
                results.append(book)
        return results

    def get_book(self, book_id: str) -> dict:
        books = self._load_books()
        for book in books:
            if book['id'] == book_id:
                return book
        return None

    def _load_books(self) -> list:
        books = []
        if not os.path.exists(BOOKS_FILE):
            return books
        with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        book = json.loads(line)
                        books.append(book)
                    except json.JSONDecodeError:
                        continue
        return books


class ReadingListManager:
    def add_book(self, username: str, book_id: str) -> bool:
        entries = self._load_reading_list()
        for entry in entries:
            if entry['username'] == username and entry['book_id'] == book_id:
                # Already in reading list
                return False
        entry = {"username": username, "book_id": book_id}
        self._save_reading_list_entry(entry)
        return True

    def get_reading_list(self, username: str) -> list:
        entries = self._load_reading_list()
        book_ids = [entry['book_id'] for entry in entries if entry['username'] == username]
        return book_ids

    def remove_book(self, username: str, book_id: str) -> bool:
        entries = self._load_reading_list()
        new_entries = [entry for entry in entries if not (entry['username'] == username and entry['book_id'] == book_id)]
        if len(new_entries) == len(entries):
            # No removal happened
            return False
        self._save_all_reading_list(new_entries)
        return True

    def _load_reading_list(self) -> list:
        entries = []
        if not os.path.exists(READING_LIST_FILE):
            return entries
        with open(READING_LIST_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entry = json.loads(line)
                        entries.append(entry)
                    except json.JSONDecodeError:
                        continue
        return entries

    def _save_reading_list_entry(self, entry: dict) -> None:
        with open(READING_LIST_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    def _save_all_reading_list(self, entries: list) -> None:
        with open(READING_LIST_FILE, 'w', encoding='utf-8') as f:
            for entry in entries:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')


class WebApp:
    def __init__(self):
        self.user_manager = UserManager()
        self.book_manager = BookManager()
        self.reading_list_manager = ReadingListManager()
        self._setup_routes()

    def _setup_routes(self):
        @app.route('/', methods=['GET', 'POST'])
        def login():
            if 'username' in session:
                return redirect(url_for('dashboard'))
            error = None
            if request.method == 'POST':
                username = request.form.get('username', '').strip()
                password = request.form.get('password', '').strip()
                if self.user_manager.login(username, password):
                    session['username'] = username
                    return redirect(url_for('dashboard'))
                else:
                    error = 'Invalid username or password.'
            return render_template('login.html', error=error)

        @app.route('/register', methods=['GET', 'POST'])
        def register():
            if 'username' in session:
                return redirect(url_for('dashboard'))
            error = None
            if request.method == 'POST':
                username = request.form.get('username', '').strip()
                password = request.form.get('password', '').strip()
                if not username or not password:
                    error = 'Username and password are required.'
                elif self.user_manager.user_exists(username):
                    error = 'Username already exists.'
                else:
                    success = self.user_manager.register(username, password)
                    if success:
                        return redirect(url_for('login'))
                    else:
                        error = 'Registration failed.'
            return render_template('register.html', error=error)

        @app.route('/dashboard', methods=['GET', 'POST'])
        def dashboard():
            if 'username' not in session:
                return redirect(url_for('login'))
            search_results = []
            query = ''
            if request.method == 'POST':
                query = request.form.get('query', '').strip()
                if query:
                    search_results = self.book_manager.search_books(query)
            return render_template('dashboard.html', username=session['username'], results=search_results, query=query)

        @app.route('/book/<book_id>', methods=['GET', 'POST'])
        def book_details(book_id):
            if 'username' not in session:
                return redirect(url_for('login'))
            book = self.book_manager.get_book(book_id)
            if not book:
                return "Book not found", 404
            message = None
            if request.method == 'POST':
                added = self.reading_list_manager.add_book(session['username'], book_id)
                if added:
                    message = 'Book added to your reading list.'
                else:
                    message = 'Book already in your reading list.'
            return render_template('book_details.html', username=session['username'], book=book, message=message)

        @app.route('/reading_list', methods=['GET', 'POST'])
        def reading_list():
            if 'username' not in session:
                return redirect(url_for('login'))
            username = session['username']
            message = None
            if request.method == 'POST':
                remove_id = request.form.get('remove_id', '').strip()
                if remove_id:
                    removed = self.reading_list_manager.remove_book(username, remove_id)
                    if removed:
                        message = 'Book removed from your reading list.'
                    else:
                        message = 'Book not found in your reading list.'
            book_ids = self.reading_list_manager.get_reading_list(username)
            books = []
            for book_id in book_ids:
                book = self.book_manager.get_book(book_id)
                if book:
                    books.append(book)
            return render_template('reading_list.html', username=username, books=books, message=message)

        @app.route('/logout')
        def logout():
            session.pop('username', None)
            return redirect(url_for('login'))

    def run(self):
        app.run(port=8291, debug=False)


if __name__ == '__main__':
    webapp = WebApp()
    webapp.run()