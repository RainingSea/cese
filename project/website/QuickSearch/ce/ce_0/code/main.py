from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, username):
        self.username = username

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
            user = User(username)
            login_user(user)
            return True
        return False

class BookManager:
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

    def search(self, query: str):
        return [book for book in self.books if query.lower() in book['title'].lower()]

    def get_book_details(self, title: str):
        for book in self.books:
            if book['title'] == title:
                return book
        return {}

class ReadingList:
    def __init__(self):
        self.reading_list = self.load_reading_list()

    def load_reading_list(self):
        reading_list = []
        if os.path.exists('reading_list.txt'):
            with open('reading_list.txt', 'r') as file:
                for line in file:
                    reading_list.append(line.strip())
        return reading_list

    def add_to_reading_list(self, book: dict):
        self.reading_list.append(book['title'])
        with open('reading_list.txt', 'a') as file:
            file.write(f"{book['title']}\n")

    def get_reading_list(self):
        return self.reading_list

user_manager = UserManager()
book_manager = BookManager()
reading_list_manager = ReadingList()

@login_manager.user_loader
def load_user(username):
    return User(username)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login_page'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_page():
    if request.method == 'POST':
        query = request.form['search']
        search_results = book_manager.search(query)
        return render_template('dashboard.html', results=search_results)
    return render_template('dashboard.html', results=[])

@app.route('/book/<title>')
@login_required
def book_details_page(title):
    book_details = book_manager.get_book_details(title)
    return render_template('book_details.html', book=book_details)

@app.route('/reading_list')
@login_required
def reading_list_page():
    return render_template('reading_list.html', reading_list=reading_list_manager.get_reading_list())

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        return redirect(url_for('dashboard_page'))
    return redirect(url_for('login_page'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(port=8398, debug=False)
