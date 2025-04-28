import os
from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from book_manager import BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

class Main:
    def __init__(self):
        self.user_manager = UserManager('users.txt')
        self.book_manager = BookManager('books.txt')
        self.user_manager.load_users()
        self.book_manager.load_books()

    def run(self):
        app.run(port=8369, debug=False)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    if main.user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/book_management')
def book_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('book_management.html', books=main.book_manager.list_books())

@app.route('/add_book', methods=['POST'])
def add_book():
    if 'username' not in session:
        return redirect(url_for('login'))
    title = request.form['title']
    author = request.form['author']
    main.book_manager.add_book(title, author)
    return redirect(url_for('book_management'))

@app.route('/user_management')
def user_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('user_management.html', users=main.user_manager.list_users())

@app.route('/register', methods=['POST'])
def register_user():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = request.form['username']
    password = request.form['password']
    if main.user_manager.register(username, password):
        return redirect(url_for('user_management'))
    return redirect(url_for('user_management'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    main = Main()
    main.run()