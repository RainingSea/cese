from flask import Flask, render_template, request, redirect, session, url_for
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
        user = User(username, password)
        user.save_to_file()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        search_query = request.form['search']
        books = Book.load_books()
        search_results = [book for book in books if search_query.lower() in book.title.lower()]
        return render_template('dashboard.html', books=search_results)
    return render_template('dashboard.html', books=[])

@app.route('/book/<book_id>')
def book_details(book_id):
    books = Book.load_books()
    book = next((b for b in books if b.title == book_id), None)
    return render_template('book_details.html', book=book)

@app.route('/add_to_reading_list/<book_id>')
def add_to_reading_list(book_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    reading_list = ReadingList(session['username'])
    reading_list.add_book(book_id)
    return redirect(url_for('reading_list'))

@app.route('/reading_list')
def reading_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    reading_list = ReadingList(session['username'])
    books = reading_list.load_reading_list()
    return render_template('reading_list.html', books=books)

if __name__ == '__main__':
    app.run(port=8589, debug=False)
