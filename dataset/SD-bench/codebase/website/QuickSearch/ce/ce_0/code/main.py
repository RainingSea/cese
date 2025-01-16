from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def register(self, username: str, password: str) -> bool:
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as f:
            users = f.readlines()
            for user in users:
                stored_username, stored_password = user.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

class Book:
    def __init__(self, title, author, summary, cover_image):
        self.title = title
        self.author = author
        self.summary = summary
        self.cover_image = cover_image

    def get_details(self) -> dict:
        return {
            "title": self.title,
            "author": self.author,
            "summary": self.summary,
            "cover_image": self.cover_image
        }

class SearchEngine:
    def search(self, query: str) -> list:
        results = []
        with open('books.txt', 'r') as f:
            books = f.readlines()
            for book in books:
                title, author, summary, cover_image = book.strip().split('|')
                if query.lower() in title.lower():
                    results.append(Book(title, author, summary, cover_image).get_details())
        return results

class ReadingList:
    def __init__(self, username: str):
        self.username = username
        self.books = []

    def add_book(self, book: Book) -> None:
        self.books.append(book)
        self.save_reading_list()

    def remove_book(self, book: Book) -> None:
        self.books.remove(book)
        self.save_reading_list()

    def get_reading_list(self) -> list:
        return self.books

    def save_reading_list(self) -> None:
        with open(f'{self.username}_reading_list.txt', 'w') as f:
            for book in self.books:
                f.write(f"{book.title}|{book.author}|{book.summary}|{book.cover_image}\n")

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
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.login(username, password):
            session['username'] = username
            return render_template('dashboard.html', username=username)
    return render_template('dashboard.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    search_engine = SearchEngine()
    results = search_engine.search(query)
    return render_template('dashboard.html', results=results)

@app.route('/book/<title>')
def book_details(title):
    with open('books.txt', 'r') as f:
        books = f.readlines()
        for book in books:
            book_title, author, summary, cover_image = book.strip().split('|')
            if book_title == title:
                return render_template('book_details.html', title=book_title, author=author, summary=summary, cover_image=cover_image)
    return redirect(url_for('dashboard'))

@app.route('/reading_list')
def reading_list():
    username = session.get('username')
    reading_list = ReadingList(username)
    return render_template('reading_list.html', books=reading_list.get_reading_list())

if __name__ == '__main__':
    app.run(port=8680, debug=False)
