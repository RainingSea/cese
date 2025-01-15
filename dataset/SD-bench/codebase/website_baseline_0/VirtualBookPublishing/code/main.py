from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from BookManager import BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
book_manager = BookManager('books.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username  # Store username in session
        return redirect(url_for('dashboard'))
    return "Invalid username or password!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Username already exists!"
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/create_book', methods=['GET', 'POST'])
def create_book():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        book_manager.create_book(title, author, content)
        return redirect(url_for('my_books'))
    return render_template('create_book.html')

@app.route('/my_books')
def my_books():
    if 'username' not in session:
        return redirect(url_for('login'))
    books = book_manager.get_books()
    return render_template('my_books.html', books=books)

@app.route('/book_details/<title>')
def book_details(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    book = book_manager.get_book_details(title)
    return render_template('book_details.html', book=book)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=8563, debug=False)
