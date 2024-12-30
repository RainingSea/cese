from flask import Flask, render_template, request, redirect, url_for, flash
from UserManager import UserManager
from BookManager import BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
book_manager = BookManager('books.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose another one.')
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
        book_manager.create_book(title, author, content)
        flash('Book created successfully!')
        return redirect(url_for('my_books'))
    return render_template('create_book.html')

@app.route('/my_books')
def my_books():
    books = book_manager.load_books()
    return render_template('my_books.html', books=books)

@app.route('/book_details/<title>')
def book_details(title):
    book = book_manager.get_book_details(title)
    return render_template('book_details.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)