from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from book import Book
from reading_list import ReadingList

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        query = request.form['query']
        books = Book.load_books()
        results = [book for book in books if query.lower() in book.title.lower()]
        return render_template('dashboard.html', books=results)
    return render_template('dashboard.html')

@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = Book.load_books()
    book = books[book_id]
    return render_template('book_details.html', book=book)

@app.route('/reading_list')
def reading_list():
    user = User.load_users()
    reading_list = ReadingList(user)
    books = reading_list.get_books()
    return render_template('reading_list.html', books=books)

if __name__ == '__main__':
    app.run(port=8681, debug=False)
