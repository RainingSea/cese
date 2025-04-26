from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self, filename):
        self.filename = filename
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class BookManager:
    def __init__(self, filename):
        self.filename = filename

    def create_book(self, username: str, title: str, author: str, content: str) -> bool:
        user_books_file = f"{username}_books.txt"
        with open(user_books_file, 'a') as file:
            file.write(f"{title}|{author}|{content}\n")
        return True

    def get_books(self, username: str) -> list:
        user_books_file = f"{username}_books.txt"
        if not os.path.exists(user_books_file):
            return []
        with open(user_books_file, 'r') as file:
            return [line.strip().split('|') for line in file]

    def get_book_details(self, username: str, title: str) -> str:
        user_books_file = f"{username}_books.txt"
        if not os.path.exists(user_books_file):
            return ""
        with open(user_books_file, 'r') as file:
            for line in file:
                book_title, author, content = line.strip().split('|')
                if book_title == title:
                    return f"Title: {book_title}\nAuthor: {author}\nContent: {content}"
        return ""

user_manager = UserManager('users.txt')
book_manager = BookManager('books.txt')

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
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/create_book', methods=['GET', 'POST'])
def create_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        book_manager.create_book(session['username'], title, author, content)
        return redirect(url_for('my_books'))
    return render_template('create_book.html')

@app.route('/my_books')
def my_books():
    books = book_manager.get_books(session['username'])
    return render_template('my_books.html', books=books)

@app.route('/book_details/<title>')
def book_details(title):
    details = book_manager.get_book_details(session['username'], title)
    return render_template('book_details.html', details=details)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=8283, debug=False)
