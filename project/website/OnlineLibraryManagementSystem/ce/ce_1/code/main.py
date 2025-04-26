from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str) -> None:
        self.users.append((username, password))
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")

    def login(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)

    def logout(self) -> None:
        session.pop('username', None)

    def list_users(self):
        return self.users

class BookManager:
    def __init__(self):
        self.books = self.load_books()

    def load_books(self):
        if not os.path.exists('books.txt'):
            return []
        with open('books.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def add_book(self, title: str, author: str) -> None:
        self.books.append((title, author))
        with open('books.txt', 'a') as file:
            file.write(f"{title}|{author}\n")

    def delete_book(self, title: str) -> None:
        self.books = [book for book in self.books if book[0] != title]
        self.save_books()

    def save_books(self):
        with open('books.txt', 'w') as file:
            for book in self.books:
                file.write(f"{book[0]}|{book[1]}\n")

    def list_books(self):
        return self.books

    def search_books(self, query: str):
        return [book for book in self.books if query.lower() in book[0].lower()]

user_manager = UserManager()
book_manager = BookManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', books=book_manager.list_books())

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def do_logout():
    user_manager.logout()
    return redirect(url_for('login'))

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    book_manager.add_book(title, author)
    return redirect(url_for('dashboard'))

@app.route('/delete_book/<title>')
def delete_book(title):
    book_manager.delete_book(title)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=8203, debug=False)
