from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from book import Book
from reading_list import ReadingList

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from file
def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users

# Load books from file
def load_books():
    books = []
    with open('books.txt', 'r') as file:
        for line in file:
            title, author, summary, cover_image = line.strip().split('|')
            books.append(Book(title, author, summary, cover_image))
    return books

# Load reading list from file
def load_reading_list(username):
    reading_list = ReadingList(User(username, ''))
    try:
        with open('reading_list.txt', 'r') as file:
            for line in file:
                user, book_title = line.strip().split('|')
                if user == username:
                    reading_list.add_book(Book(book_title, '', '', ''))
    except FileNotFoundError:
        pass
    return reading_list

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username not in users:
            with open('users.txt', 'a') as file:
                file.write(f"{username}|{password}\n")
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('search_books'))
    return render_template('login.html')

@app.route('/search_books')
def search_books():
    books = load_books()
    return render_template('dashboard.html', books=books)

@app.route('/book_details/<title>')
def book_details(title):
    books = load_books()
    selected_book = next((book for book in books if book.title == title), None)
    return render_template('book_details.html', book=selected_book)

@app.route('/reading_list')
def reading_list():
    username = session.get('username')
    reading_list = load_reading_list(username)
    return render_template('reading_list.html', reading_list=reading_list)

if __name__ == '__main__':
    app.run(port=8683, debug=False)
