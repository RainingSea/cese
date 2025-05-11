from flask import Flask, render_template, request, redirect, session, flash
from UserManager import UserManager
from BookManager import BookManager
from Session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

user_manager = UserManager()
book_manager = BookManager()
session_manager = Session()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session_manager.set_user(username)
            session['username'] = username
            flash('Login successful.')
            return redirect('/dashboard')
        else:
            flash('Invalid credentials. Please try again.')
            return redirect('/')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if session_manager.get_user():
        return render_template('dashboard.html')
    return redirect('/')

@app.route('/logout')
def logout():
    session_manager.clear_user()
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect('/')

@app.route('/books', methods=['GET', 'POST'])
def book_management():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        if book_manager.add_book(title, author):
            flash('Book added successfully.')
        else:
            flash('Book already exists.')
    books = book_manager.view_books()
    return render_template('book_management.html', books=books)

@app.route('/users', methods=['GET', 'POST'])
def user_management():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('User registered successfully.')
        else:
            flash('Username already exists.')
    users = user_manager.load_users()
    return render_template('user_management.html', users=users)

@app.route('/search_books', methods=['POST'])
def search_books():
    query = request.form['query']
    results = book_manager.search_books(query)
    return render_template('book_management.html', books=results)

if __name__ == '__main__':
    user_manager.load_users()
    book_manager.load_books()
    app.run(port=8480, debug=False)
