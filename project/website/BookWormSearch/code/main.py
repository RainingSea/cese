from flask import Flask, render_template, request, redirect, url_for, session
import os
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class Book:
    def __init__(self, title, author, summary, description):
        self.title = title
        self.author = author
        self.summary = summary
        self.description = description

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()

    def user_exists(self, username):
        with open(self.users_file, 'r') as f:
            for line in f:
                existing_username, _ = line.strip().split('|')
                if existing_username == username:
                    return True
        return False

    def register(self, username, password):
        if self.user_exists(username):
            return False
        
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username, password):
        user_found = False
        with open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    existing_username, existing_password = parts
                    if existing_username == username:
                        user_found = True
                        if existing_password == password:
                            return True
        return False if not user_found else False

class BookManager:
    def __init__(self, books_file='books.txt'):
        self.books_file = books_file
        if not os.path.exists(self.books_file):
            open(self.books_file, 'w').close()

    def search(self, query):
        results = []
        with open(self.books_file, 'r') as f:
            for line in f:
                title, author, summary, description = line.strip().split('|')
                if query.lower() in title.lower() or query.lower() in author.lower():
                    results.append(Book(title, author, summary, description))
        return results

    def get_book_details(self, title):
        with open(self.books_file, 'r') as f:
            for line in f:
                book_title, author, summary, description = line.strip().split('|')
                if book_title == title:
                    return Book(book_title, author, summary, description)
        return None

class ReadingListManager:
    def __init__(self, lists_file='reading_lists.txt'):
        self.lists_file = lists_file
        if not os.path.exists(self.lists_file):
            open(self.lists_file, 'w').close()

    def add_book(self, username, book_title):
        with open(self.lists_file, 'r') as f:
            for line in f:
                existing_user, existing_title = line.strip().split('|')
                if existing_user == username and existing_title == book_title:
                    return False
        
        with open(self.lists_file, 'a') as f:
            f.write(f"{username}|{book_title}\n")
        return True

    def get_list(self, username):
        books = []
        with open(self.lists_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    existing_user, book_title = parts
                    if existing_user == username:
                        books.append(book_title)
        return books

    def remove_book(self, username, book_title):
        lines = []
        removed = False
        with open(self.lists_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    existing_user, existing_title = parts
                    if existing_user == username and existing_title == book_title:
                        removed = True
                    else:
                        lines.append(line)
        
        if removed:
            with open(self.lists_file, 'w') as f:
                f.writelines(lines)
        return removed

user_manager = UserManager()
book_manager = BookManager()
reading_list_manager = ReadingListManager()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not user_manager.user_exists(username):
            return render_template('login.html', error='User not found')
        
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        query = request.form['query']
        books = book_manager.search(query)
        return render_template('dashboard.html', books=books, username=session['username'])
    
    return render_template('dashboard.html', username=session['username'])

@app.route('/book_details/<title>', methods=['GET', 'POST'])
def book_details(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    book = book_manager.get_book_details(title)
    if not book:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        if reading_list_manager.add_book(session['username'], book.title):
            return redirect(url_for('reading_list'))
    
    return render_template('book_details.html', book=book, username=session['username'])

@app.route('/reading_list')
def reading_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    book_titles = reading_list_manager.get_list(session['username'])
    books = []
    for title in book_titles:
        book = book_manager.get_book_details(title)
        if book:
            books.append(book)
    
    return render_template('reading_list.html', books=books, username=session['username'])

@app.route('/remove_from_list/<title>')
def remove_from_list(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    reading_list_manager.remove_book(session['username'], title)
    return redirect(url_for('reading_list'))

@app.route('/logout')
def logout():
    session.clear()
    time.sleep(0.5)  # Ensure session is cleared
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8563, debug=False)
