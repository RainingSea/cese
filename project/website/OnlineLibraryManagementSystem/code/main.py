from flask import Flask, render_template, request, redirect, url_for, session, flash
from user_management import UserManager
from book_management import BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
book_manager = BookManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    flash('Invalid username or password.')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    user_manager.logout()
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/book_management')
def book_management():
    books = book_manager.view_books()
    return render_template('book_management.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    if book_manager.add_book(title, author):
        flash('Book added successfully.')
    else:
        flash('Book already exists.')
    return redirect(url_for('book_management'))

@app.route('/delete_book/<title>', methods=['POST'])
def delete_book(title):
    if book_manager.delete_book(title):
        flash('Book deleted successfully.')
    else:
        flash('Book not found.')
    return redirect(url_for('book_management'))

@app.route('/user_management')
def user_management():
    users = user_manager.users
    return render_template('user_management.html', users=users)

@app.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    if user_manager.register(username, password):
        flash('User registered successfully.')
    else:
        flash('Username already exists.')
    return redirect(url_for('user_management'))

@app.route('/search_books', methods=['GET', 'POST'])
def search_books():
    results = []
    if request.method == 'POST':
        query = request.form['query']
        results = book_manager.search_books(query)
    return render_template('search_books.html', results=results)

if __name__ == '__main__':
    user_manager.load_users()
    book_manager.load_books()
    app.run(port=8483, debug=False)
