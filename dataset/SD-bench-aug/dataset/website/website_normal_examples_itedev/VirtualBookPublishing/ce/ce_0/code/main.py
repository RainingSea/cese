from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from book_manager import BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
book_manager = BookManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return render_template('registration.html', error="Username already exists.")
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/create_book', methods=['GET', 'POST'])
def create_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        book_manager.add_book(title, author, content)
        return redirect(url_for('my_books'))
    return render_template('create_book.html')

@app.route('/my_books')
def my_books():
    books = book_manager.get_books()
    return render_template('my_books.html', books=books)

@app.route('/book_details/<title>')
def book_details(title):
    book = book_manager.get_book_details(title)
    return render_template('book_details.html', book=book)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    user_manager.load_users()
    book_manager.load_books()
    app.run(debug=True)