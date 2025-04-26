import os
from user_manager import UserManager
from book_manager import BookManager
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
book_manager = BookManager('books.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        books = book_manager.list_books()
        return render_template('dashboard.html', username=session['username'], books=books)
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Login Failed"

@app.route('/logout')
def logout():
    user_manager.logout()
    return redirect(url_for('login'))

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    if book_manager.add_book(title, author):
        return redirect(url_for('dashboard'))
    return "Failed to add book"

@app.route('/delete_book', methods=['POST'])
def delete_book():
    title = request.form['title']
    if book_manager.delete_book(title):
        return redirect(url_for('dashboard'))
    return "Failed to delete book"

@app.route('/list_books')
def list_books():
    books = book_manager.list_books()
    return render_template('book_management.html', books=books)

@app.route('/search_books', methods=['POST'])
def search_books():
    if request.method == 'POST':
        query = request.form['query']
        results = book_manager.search_book(query)
        return render_template('search.html', results=results)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=8205, debug=False)
