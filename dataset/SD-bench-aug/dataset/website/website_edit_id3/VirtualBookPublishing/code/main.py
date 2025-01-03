from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

USERS_FILE = 'users.txt'
BOOKS_FILE = 'books.txt'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Book:
    def __init__(self, title: str, author: str, content: str):
        self.title = title
        self.author = author
        self.content = content

def load_users():
    users = []
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                users.append(User(username, password))
    return users

def load_books():
    books = []
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, 'r') as file:
            for line in file:
                try:
                    title, author, content = line.strip().split(';', 2)  # Limit splits to 2
                    books.append(Book(title, author, content))
                except ValueError:
                    print(f"Skipping malformed entry in books.txt: {line.strip()}")
    return books

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            with open(USERS_FILE, 'a') as file:
                file.write(f"{username},{password}\n")
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    for user in users:
        if user.username == username and user.password == password:
            return redirect(url_for('dashboard'))
    flash('Invalid username or password.')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/create_book', methods=['GET', 'POST'])
def create_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        if title and author and content:
            with open(BOOKS_FILE, 'a') as file:
                file.write(f"{title};{author};{content}\n")
            flash('Book created successfully!')
            return redirect(url_for('dashboard'))
        else:
            flash('All fields are required to create a book.')
    return render_template('create_book.html')

@app.route('/my_books')
def my_books():
    books = load_books()
    return render_template('my_books.html', books=books)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = load_books()
    if 0 <= book_id < len(books):
        book = books[book_id]
        return render_template('book_details.html', book=book)
    flash('Book not found.')
    return redirect(url_for('my_books'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=8146, debug=True)
