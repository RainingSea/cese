from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from book_manager import BookManager
from user import User
from book import Book

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
book_manager = BookManager('books.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

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
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/create_book', methods=['GET', 'POST'])
def create_book():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        book = Book(session['username'], title, author, content)
        book_manager.add_book(book)
        return redirect(url_for('my_books'))
    return render_template('create_book.html')

@app.route('/my_books')
def my_books():
    if 'username' not in session:
        return redirect(url_for('login'))
    books = book_manager.get_books_by_user(session['username'])
    return render_template('my_books.html', books=books)

@app.route('/book_details/<title>')
def book_details(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    book = book_manager.get_book_details(title, session['username'])
    return render_template('book_details.html', book=book)

if __name__ == '__main__':
    app.run(port=8077, debug=False)
