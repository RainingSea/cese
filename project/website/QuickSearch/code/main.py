from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username] == password:
            session['username'] = username
            return True
        return False

class SearchEngine:
    def __init__(self):
        self.books = self.load_books()

    def load_books(self):
        books = []
        if os.path.exists('books.txt'):
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author, summary, cover_image = line.strip().split('|')
                    books.append({'title': title, 'author': author, 'summary': summary, 'cover_image': cover_image})
        return books

    def search(self, query: str) -> list:
        results = [book for book in self.books if query.lower() in book['title'].lower()]
        return results if results else None

    def get_book_details(self, title: str) -> dict:
        for book in self.books:
            if book['title'] == title:
                return book
        return {}

class ReadingListManager:
    def __init__(self):
        self.reading_list = self.load_reading_list()

    def load_reading_list(self):
        reading_list = {}
        if os.path.exists('reading_list.txt'):
            with open('reading_list.txt', 'r') as file:
                for line in file:
                    username, book_title = line.strip().split('|')
                    if username not in reading_list:
                        reading_list[username] = []
                    reading_list[username].append(book_title)
        return reading_list

    def add_to_reading_list(self, username: str, book_title: str) -> bool:
        if username not in self.reading_list:
            self.reading_list[username] = []
        if book_title in self.reading_list[username]:
            return False
        self.reading_list[username].append(book_title)
        with open('reading_list.txt', 'a') as file:
            file.write(f"{username}|{book_title}\n")
        return True

    def remove_from_reading_list(self, username: str, book_title: str) -> bool:
        if username in self.reading_list and book_title in self.reading_list[username]:
            self.reading_list[username].remove(book_title)
            self.save_reading_list()
            return True
        return False

    def get_reading_list(self, username: str) -> list:
        return self.reading_list.get(username, [])

    def save_reading_list(self):
        with open('reading_list.txt', 'w') as file:
            for username, books in self.reading_list.items():
                for book in books:
                    file.write(f"{username}|{book}\n")

user_manager = UserManager()
search_engine = SearchEngine()
reading_list_manager = ReadingListManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different one.')
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    username = session.get('username')
    if request.method == 'POST':
        if username:
            query = request.form['query']
            results = search_engine.search(query)
            if results is None:
                flash('No results found.')
                results = search_engine.books  # Show all books if no results found
            return render_template('dashboard.html', books=results, username=username)
        else:
            username = request.form['username']
            password = request.form['password']
            if user_manager.login(username, password):
                return render_template('dashboard.html', books=search_engine.books, username=username)
            else:
                flash('Invalid username or password.')
    if username:
        return render_template('dashboard.html', books=search_engine.books, username=username)
    return redirect(url_for('login'))

@app.route('/book/<title>')
def book_details(title):
    book = search_engine.get_book_details(title)
    return render_template('book_details.html', book=book)

@app.route('/add_to_reading_list', methods=['POST'])
def add_to_reading_list():
    username = session.get('username')
    book_title = request.form['book_title']
    if username:
        if reading_list_manager.add_to_reading_list(username, book_title):
            flash(f'Added {book_title} to your reading list.')
        else:
            flash(f'{book_title} is already in your reading list.')
    else:
        flash('You need to log in to add books to your reading list.')
    return redirect(url_for('dashboard'))

@app.route('/reading_list/<username>')
def reading_list(username):
    books = reading_list_manager.get_reading_list(username)
    return render_template('reading_list.html', books=books, username=username)

@app.route('/remove_from_reading_list', methods=['POST'])
def remove_from_reading_list():
    username = request.form['username']
    book_title = request.form['book_title']
    if reading_list_manager.remove_from_reading_list(username, book_title):
        flash(f'Removed {book_title} from your reading list.')
    else:
        flash(f'{book_title} is not in your reading list.')
    return redirect(url_for('reading_list', username=username))

if __name__ == '__main__':
    app.run(port=8229, debug=False)
