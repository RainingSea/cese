from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from book import Book
from reading_list import ReadingList

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from file
def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users

# Load books from file
def load_books():
    books = []
    with open('books.txt', 'r') as file:
        for line in file:
            title, author, summary = line.strip().split('|')
            books.append(Book(title, author, summary))
    return books

# Load reading lists from file
def load_reading_lists():
    reading_lists = {}
    with open('reading_list.txt', 'r') as file:
        for line in file:
            username, books = line.strip().split('|')
            reading_lists[username] = books.split(',')
    return reading_lists

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            return render_template('dashboard.html', books=load_books())
    return redirect(url_for('login'))

@app.route('/book/<title>')
def book_details(title):
    books = load_books()
    for book in books:
        if book.title == title:
            return render_template('book_details.html', book=book.get_details())
    return redirect(url_for('dashboard'))

@app.route('/reading_list')
def reading_list():
    if 'username' in session:
        reading_lists = load_reading_lists()
        user_reading_list = reading_lists.get(session['username'], [])
        return render_template('reading_list.html', books=user_reading_list)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8588, debug=False)
