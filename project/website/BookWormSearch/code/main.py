from flask import Flask, render_template, request, redirect, url_for, session, flash
from user_manager import UserManager
from book_manager import BookManager
from reading_list_manager import ReadingListManager
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
book_manager = BookManager('books.txt')
reading_list_manager = ReadingListManager('reading_list.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already taken. Please choose another.', 'error')
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    books = []
    if request.method == 'POST':
        query = request.form['query']
        books = book_manager.search_books(query)
    
    return render_template('dashboard.html', books=books)

@app.route('/book/<title>')
def book_details(title):
    book_details = book_manager.get_book_details(title)
    if not book_details:
        flash('Book not found.', 'error')
        return redirect(url_for('dashboard'))
    return render_template('book_details.html', book=book_details)

@app.route('/reading_list')
def reading_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    books = reading_list_manager.get_reading_list(session['username'])
    return render_template('reading_list.html', books=books)

@app.route('/add_to_reading_list/<title>')
def add_to_reading_list(title):
    if 'username' in session:
        if reading_list_manager.add_to_reading_list(session['username'], title):
            flash(f'Added "{title}" to your reading list.', 'success')
        else:
            flash(f'"{title}" is already in your reading list.', 'error')
    return redirect(url_for('reading_list'))

@app.route('/remove_from_reading_list/<title>')
def remove_from_reading_list(title):
    if 'username' in session:
        if reading_list_manager.remove_from_reading_list(session['username'], title):
            flash(f'Removed "{title}" from your reading list.', 'success')
        else:
            flash(f'"{title}" is not in your reading list.', 'error')
    return redirect(url_for('reading_list'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    flash('Invalid username or password. Please try again.', 'error')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8302, debug=False)
