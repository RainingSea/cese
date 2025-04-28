from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self, filename):
        self.filename = filename

    def register(self, username: str, password: str) -> bool:
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        with open(self.filename, 'r') as file:
            for line in file:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

class BookManager:
    def __init__(self, filename):
        self.filename = filename

    def create_book(self, username: str, title: str, author: str, content: str) -> bool:
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{title}|{author}|{content}\n")
        return True

    def get_books(self, username: str) -> list:
        books = []
        with open(self.filename, 'r') as file:
            for line in file:
                stored_username, title, author, content = line.strip().split('|')
                if stored_username == username:
                    books.append((title, author))
        return books

    def get_book_details(self, username: str, title: str) -> str:
        with open(self.filename, 'r') as file:
            for line in file:
                stored_username, stored_title, author, content = line.strip().split('|')
                if stored_username == username and stored_title == title:
                    return f"Title: {stored_title}, Author: {author}, Content: {content}"
        return "Book not found."

user_manager = UserManager('users.txt')
book_manager = BookManager('books.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.register(username, password)
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
        username = session.get('username')
        book_manager.create_book(username, title, author, content)
        return redirect(url_for('my_books'))
    return render_template('create_book.html')

@app.route('/my_books')
def my_books():
    username = session.get('username')
    books = book_manager.get_books(username)
    return render_template('my_books.html', books=books)

@app.route('/book_details/<title>')
def book_details(title):
    username = session.get('username')
    details = book_manager.get_book_details(username, title)
    return render_template('book_details.html', details=details)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=8455, debug=False)
