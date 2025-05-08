from flask import Flask, render_template, request, redirect, session, url_for, flash
from user_manager import UserManager
from book_manager import BookManager
from reading_list_manager import ReadingListManager
import time
import threading

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

user_manager = UserManager('users.txt')
book_manager = BookManager('books.txt')

# Function to check if the app is ready
def wait_for_app_ready():
    time.sleep(2)  # Wait for 2 seconds to allow the app to initialize

@app.before_first_request
def startup():
    threading.Thread(target=wait_for_app_ready).start()

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
            flash('Username already exists. Please choose a different one.')
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        query = request.form['query']
        books = book_manager.search_books(query)
        return render_template('dashboard.html', books=books)
    
    # Display all books when no search query is provided
    books = book_manager.get_all_books()
    return render_template('dashboard.html', books=books)

@app.route('/book/<title>')
def book_details(title):
    book = book_manager.get_book_details(title)
    return render_template('book_details.html', book=book)

@app.route('/reading_list', methods=['GET', 'POST'])
def reading_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    reading_list_manager = ReadingListManager(f"{session['username']}_reading_list.txt")
    reading_list = reading_list_manager.get_reading_list(session['username'])
    
    if request.method == 'POST':
        book_title = request.form['book_title']
        reading_list_manager.add_to_reading_list(session['username'], book_title)
        return redirect(url_for('reading_list'))

    return render_template('reading_list.html', reading_list=reading_list)

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
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8292, debug=False)
