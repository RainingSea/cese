from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self, username: str, password: str) -> bool:
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as file:
            for line in file:
                user_data = line.strip().split('|')
                if user_data[0] == username and user_data[1] == password:
                    return True
        return False

class Book:
    def __init__(self, title: str, author: str, summary: str):
        self.title = title
        self.author = author
        self.summary = summary

    def get_details(self) -> dict:
        return {
            'title': self.title,
            'author': self.author,
            'summary': self.summary
        }

class ReadingList:
    def __init__(self, user: User):
        self.user = user
        self.books = []

    def add_book(self, book: Book) -> None:
        self.books.append(book)

    def remove_book(self, book: Book) -> None:
        self.books.remove(book)

    def get_books(self) -> list:
        return [book.get_details() for book in self.books]

class BookSearch:
    def __init__(self):
        self.books = self.load_books()

    def load_books(self) -> list:
        books = []
        with open('books.txt', 'r') as file:
            for line in file:
                title, author, summary = line.strip().split('|')
                books.append(Book(title, author, summary))
        return books

    def search(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book.title.lower()]

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.register(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.login(username, password):
            session['username'] = username
            return render_template('dashboard.html', books=BookSearch().books)
    return render_template('login.html')

@app.route('/book/<title>')
def book_details(title):
    book_search = BookSearch()
    for book in book_search.books:
        if book.title == title:
            return render_template('book_details.html', book=book.get_details())
    return redirect(url_for('dashboard'))

@app.route('/reading_list')
def reading_list():
    return render_template('reading_list.html')

if __name__ == '__main__':
    app.run(port=8994, debug=False)
