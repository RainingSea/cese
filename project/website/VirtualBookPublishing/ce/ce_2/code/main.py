from flask import Flask, render_template, request, redirect, url_for, session
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def register(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    def login(self):
        with open('users.txt', 'r') as f:
            users = f.readlines()
            for user in users:
                u, p = user.strip().split('|')
                if u == self.username and p == self.password:
                    return True
        return False

class Book:
    def __init__(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content

    def save(self):
        with open('books.txt', 'a') as f:
            f.write(f"{self.title}|{self.author}|{self.content}\n")

    def get_details(self):
        return f"Title: {self.title}\nAuthor: {self.author}\nContent: {self.content}"

def load_users():
    users = []
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    return users

def load_books():
    books = []
    if os.path.exists('books.txt'):
        with open('books.txt', 'r') as f:
            for line in f:
                title, author, content = line.strip().split('|')
                books.append(Book(title, author, content))
    return books

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    new_user = User(username, password)
    new_user.register()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/create_book', methods=['POST'])
def create_book():
    title = request.form['title']
    author = request.form['author']
    content = request.form['content']
    new_book = Book(title, author, content)
    new_book.save()
    return redirect(url_for('my_books'))

@app.route('/my_books')
def my_books():
    books = load_books()
    return render_template('my_books.html', books=books)

@app.route('/book_details/<int:book_id>')
def book_details(book_id):
    books = load_books()
    if 0 <= book_id < len(books):
        book = books[book_id]
        return render_template('book_details.html', book=book)
    return redirect(url_for('my_books'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=8284, debug=False)
