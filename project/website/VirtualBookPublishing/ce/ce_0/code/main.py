from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from book_manager import BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
book_manager = BookManager('books.txt')

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
            return "Registration failed. Username may already exist."
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Login failed. Check your username and password."

@app.route('/create_book', methods=['GET', 'POST'])
def create_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        book_manager.create_book(title, author, content)
        return redirect(url_for('my_books'))
    return render_template('create_book.html')

@app.route('/my_books', methods=['GET'])
def my_books():
    books = book_manager.get_all_books()
    return render_template('my_books.html', books=books)

@app.route('/book_details/<title>', methods=['GET'])
def book_details(title):
    details = book_manager.get_book_details(title)
    return render_template('book_details.html', details=details)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8689, debug=False)
