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
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append({'username': username, 'password': password})
        return users

    def register(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password})
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return True
        return False

class BookManager:
    def __init__(self):
        self.books = self.load_books()

    def load_books(self):
        books = []
        if os.path.exists('books.txt'):
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author = line.strip().split('|')
                    books.append({'title': title, 'author': author})
        return books

    def search(self, query: str):
        return [book for book in self.books if query.lower() in book['title'].lower() or query.lower() in book['author'].lower()]

    def add_to_reading_list(self, book_id: str, user_id: str) -> bool:
        # Placeholder for adding to reading list logic
        return True

    def get_reading_list(self, user_id: str):
        # Placeholder for getting reading list logic
        return []

user_manager = UserManager()
book_manager = BookManager()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        return redirect('/dashboard')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', books=book_manager.books)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if user_manager.register(username, password):
        return redirect('/')
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8293, debug=False)
