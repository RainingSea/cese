from flask import Flask, render_template, request, redirect, url_for, session
from library import Library
from user import User
from book import Book

app = Flask(__name__)
app.secret_key = 'your_secret_key'
library = Library()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    for user in library.view_users():
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    return "Invalid credentials", 401

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/load_data')
def load_data():
    library.load_users_from_file('users.txt')
    library.load_books_from_file('books.txt')
    return "Data loaded successfully"

if __name__ == '__main__':
    app.run(port=8663, debug=False)
