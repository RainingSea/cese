from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from book import Book

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from the file
def load_users():
    users = []
    try:
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    except FileNotFoundError:
        pass
    return users

# Load books from the file
def load_books():
    books = []
    try:
        with open('books.txt', 'r') as f:
            for line in f:
                title, author, content = line.strip().split('|')
                books.append(Book(title, author, content))
    except FileNotFoundError:
        pass
    return books

users = load_users()
books = load_books()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        users.append(new_user)
        new_user.save()
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
        new_book = Book(title, author, content)
        books.append(new_book)
        new_book.save()
        return redirect(url_for('my_books'))
    return render_template('create_book.html')

@app.route('/my_books')
def my_books():
    return render_template('my_books.html', books=books)

@app.route('/book/<title>')
def book_details(title):
    for book in books:
        if book.title == title:
            return render_template('book_details.html', book=book)
    return redirect(url_for('my_books'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=8693, debug=False)
