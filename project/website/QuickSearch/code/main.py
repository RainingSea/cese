from flask import Flask, render_template, request, redirect, url_for, session, flash
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
            flash('Registration successful!')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username may already exist.')
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    search_results = []
    if request.method == 'POST':
        query = request.form['query']
        search_results = book_manager.search_books(query)
    
    return render_template('dashboard.html', results=search_results)

@app.route('/book/<title>')
def book_details(title):
    book = book_manager.get_book_details(title)
    if not book:
        flash('Book not found.')
        return redirect(url_for('dashboard'))
    return render_template('book_details.html', book=book)

@app.route('/add_to_reading_list/<title>')
def add_to_reading_list(title):
    if 'username' in session:
        user_manager.add_to_reading_list(session['username'], title)
        flash('Book added to your reading list!')
    else:
        flash('You need to log in to add books to your reading list.')
    return redirect(url_for('dashboard'))

@app.route('/reading_list')
def reading_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    reading_list = user_manager.get_reading_list(session['username'])
    return render_template('reading_list.html', reading_list=reading_list)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        flash('Login failed. Check your username and password.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8401, debug=False)
