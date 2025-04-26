from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

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
                    title, author, summary, cover_image, description = line.strip().split('|')
                    books.append({
                        'title': title,
                        'author': author,
                        'summary': summary,
                        'cover_image': cover_image,
                        'description': description
                    })
        return books

    def search(self, query: str):
        return [book for book in self.books if query.lower() in book['title'].lower()]

    def get_book_details(self, title: str):
        for book in self.books:
            if book['title'] == title:
                return book
        return {}

class ReadingList:
    def __init__(self):
        self.reading_lists = self.load_reading_lists()

    def load_reading_lists(self):
        reading_lists = {}
        if os.path.exists('reading_list.txt'):
            with open('reading_list.txt', 'r') as file:
                for line in file:
                    username, book_title = line.strip().split('|')
                    if username not in reading_lists:
                        reading_lists[username] = []
                    reading_lists[username].append(book_title)
        return reading_lists

    def add_to_reading_list(self, username: str, book_title: str) -> bool:
        if username not in self.reading_lists:
            self.reading_lists[username] = []
        if book_title in self.reading_lists[username]:
            return False
        self.reading_lists[username].append(book_title)
        with open('reading_list.txt', 'a') as file:
            file.write(f"{username}|{book_title}\n")
        return True

    def get_reading_list(self, username: str):
        return self.reading_lists.get(username, [])

user_manager = UserManager()
search_engine = SearchEngine()
reading_list_manager = ReadingList()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if user_manager.register(username, password):
        return redirect('/login')
    return "Registration failed", 400

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        return redirect('/dashboard')
    return "Login failed", 400

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = search_engine.search(query)
    return render_template('dashboard.html', results=results)

@app.route('/book/<title>')
def book_details(title):
    book = search_engine.get_book_details(title)
    return render_template('book_details.html', book=book)

@app.route('/add_to_reading_list/<title>')
def add_to_reading_list(title):
    username = session.get('username')
    if username:
        reading_list_manager.add_to_reading_list(username, title)
        return redirect('/reading_list')
    return "User not logged in", 403

@app.route('/reading_list')
def reading_list():
    username = session.get('username')
    if username:
        books = reading_list_manager.get_reading_list(username)
        return render_template('reading_list.html', books=books)
    return "User not logged in", 403

if __name__ == '__main__':
    app.run(port=8228, debug=False)
