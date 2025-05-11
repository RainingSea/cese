from flask import Flask, render_template, request, redirect, session, flash
from UserManager import UserManager
from BookManager import BookManager
from SessionManager import SessionManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
book_manager = BookManager()
session_manager = SessionManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session_manager.is_logged_in():
        return redirect('/')
    return render_template('dashboard.html', username=session_manager.get_current_user())

@app.route('/logout')
def logout():
    user_manager.logout()
    session.clear()
    return redirect('/')

@app.route('/book_management', methods=['GET', 'POST'])
def book_management():
    if not session_manager.is_logged_in():
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        if book_manager.add_book(title, author, int(year)):
            flash('Book added successfully.')
        else:
            flash('Failed to add book.')
    books = book_manager.get_books()
    return render_template('book_management.html', books=books)

@app.route('/user_management', methods=['GET', 'POST'])
def user_management():
    if not session_manager.is_logged_in():
        return redirect('/')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('User registered successfully.')
        else:
            flash('Username already exists.')
    users = user_manager.get_users()
    return render_template('user_management.html', users=users)

@app.route('/search_books', methods=['GET', 'POST'])
def search_books():
    if not session_manager.is_logged_in():
        return redirect('/')
    if request.method == 'POST':
        query = request.form['query']
        results = book_manager.search_books(query)
        return render_template('search_books.html', results=results)
    return render_template('search_books.html', results=[])

if __name__ == '__main__':
    app.run(port=8482, debug=False)
