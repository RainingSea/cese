from flask import Flask, render_template, request, redirect, session
from user import User
from book import Book
from reading_list import ReadingList

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and books from files
def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users

def load_books():
    books = []
    with open('books.txt', 'r') as file:
        for line in file:
            title, author, summary = line.strip().split('|')
            books.append(Book(title, author, summary))
    return books

users_data = load_users()
books_data = load_books()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users_data:
            users_data[username] = password
            with open('users.txt', 'a') as file:
                file.write(f"{username}|{password}\n")
            return redirect('/')
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users_data and users_data[username] == password:
            session['username'] = username
            return render_template('dashboard.html', books=books_data)
    return redirect('/')

@app.route('/book/<int:book_id>')
def book_details(book_id):
    book = books_data[book_id]
    return render_template('book_details.html', book=book)

@app.route('/reading_list')
def reading_list():
    return render_template('reading_list.html')

if __name__ == '__main__':
    app.run(port=8996, debug=False)
