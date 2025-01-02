from flask import Flask, render_template, request, redirect, session, url_for
from user import User
from book import Book

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Load users from the text file
def load_users():
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split(':')
                users.append(User(username, password))
    except FileNotFoundError:
        pass
    return users

# Load books from the text file
def load_books():
    books = []
    try:
        with open('books.txt', 'r') as file:
            for line in file:
                username, title, author, content = line.strip().split(':')
                books.append(Book(username, title, author, content))
    except FileNotFoundError:
        pass
    return books

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
        return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/create_book')
def create_book():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('create_book.html')

@app.route('/my_books')
def my_books():
    if 'username' not in session:
        return redirect(url_for('login'))
    books = load_books()
    user_books = [book for book in books if book.username == session['username']]
    return render_template('my_books.html', books=user_books)

@app.route('/book_details/<title>')
def book_details(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    books = load_books()
    selected_book = next((book for book in books if book.title == title and book.username == session['username']), None)
    if selected_book:
        return render_template('book_details.html', book=selected_book)
    return "Book not found."

if __name__ == '__main__':
    app.run(port=8156, debug=True)
