from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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
        return self.users.get(username) == password

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
        return None

    def add_to_reading_list(self, username: str, book_title: str) -> bool:
        if not os.path.exists('reading_list.txt'):
            with open('reading_list.txt', 'w') as file:
                pass
        with open('reading_list.txt', 'a') as file:
            file.write(f"{username}|{book_title}\n")
        return True

    def get_reading_list(self, username: str):
        reading_list = []
        if os.path.exists('reading_list.txt'):
            with open('reading_list.txt', 'r') as file:
                for line in file:
                    user, book_title = line.strip().split('|')
                    if user == username:
                        reading_list.append(book_title)
        return reading_list

user_manager = UserManager()
book_manager = BookManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Username already exists."
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        query = request.form['query']
        search_results = book_manager.search(query)
        return render_template('dashboard.html', books=search_results)
    return render_template('dashboard.html')

@app.route('/book/<title>')
def book_details(title):
    book = book_manager.get_book_details(title)
    return render_template('book_details.html', book=book)

@app.route('/add_to_reading_list/<title>')
def add_to_reading_list(title):
    if 'username' in session:
        book_manager.add_to_reading_list(session['username'], title)
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/reading_list')
def reading_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    books = book_manager.get_reading_list(session['username'])
    return render_template('reading_list.html', books=books)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Invalid credentials."

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8399, debug=False)
