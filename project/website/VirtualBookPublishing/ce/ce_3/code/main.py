from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from book import Book

app = Flask(__name__)
app.secret_key = 'your_secret_key'
users = User().load_users()
books = Book().load_books()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User().register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/create_book', methods=['GET', 'POST'])
def create_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        Book().create_book(title, author, content)
        return redirect(url_for('my_books'))
    return render_template('create_book.html')

@app.route('/my_books')
def my_books():
    return render_template('my_books.html', books=books)

@app.route('/book_details/<title>')
def book_details(title):
    book = Book().view_book_details(title)
    return render_template('book_details.html', book=book)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=8692, debug=False)
