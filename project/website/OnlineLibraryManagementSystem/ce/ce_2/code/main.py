from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username:
                return False
        self.users.append([username, password])
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                session['username'] = username
                return True
        return False

    def logout(self):
        session.pop('username', None)

    def view_users(self):
        return self.users

class BookManager:
    def __init__(self):
        self.books = self.load_books()

    def load_books(self):
        if not os.path.exists('books.txt'):
            return []
        with open('books.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def add_book(self, title: str, author: str) -> bool:
        self.books.append([title, author])
        self.save_books()
        return True

    def delete_book(self, title: str) -> bool:
        for book in self.books:
            if book[0] == title:
                self.books.remove(book)
                self.save_books()
                return True
        return False

    def save_books(self):
        with open('books.txt', 'w') as file:
            for book in self.books:
                file.write('|'.join(book) + '\n')

    def view_books(self):
        return self.books

    def search_books(self, query: str):
        return [book for book in self.books if query.lower() in book[0].lower()]

user_manager = UserManager()
book_manager = BookManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/logout')
def logout():
    user_manager.logout()
    return redirect('/')

@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        book_manager.add_book(title, author)
    return render_template('book_management.html', books=book_manager.view_books())

@app.route('/users')
def users():
    return render_template('user_management.html', users=user_manager.view_users())

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        query = request.form['query']
        results = book_manager.search_books(query)
    return render_template('search.html', results=results)

if __name__ == '__main__':
    app.run(port=8204, debug=False)
