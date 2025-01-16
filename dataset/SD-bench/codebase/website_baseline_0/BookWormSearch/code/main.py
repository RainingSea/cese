from flask import Flask, render_template, request, redirect, url_for, session, flash
from user import User
from book import Book
from reading_list import ReadingList

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and books from files
def load_users():
    return User.load_all()

def load_books():
    return Book.load_all()

users = load_users()
books = load_books()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username already exists
        if any(user.username == username for user in users):
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
        
        new_user = User(username, password)
        new_user.save()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        search_query = request.form['search']
        filtered_books = [book for book in books if search_query.lower() in book.title.lower()]
        return render_template('dashboard.html', books=filtered_books)
    
    return render_template('dashboard.html', books=books)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    book = books[book_id]
    return render_template('book_details.html', book=book)

@app.route('/reading_list', methods=['GET', 'POST'])
def reading_list():
    user = session.get('user')
    reading_list = ReadingList(user)
    if request.method == 'POST':
        book_id = int(request.form['book_id'])
        reading_list.add_book(books[book_id])
        flash(f'Added {books[book_id].title} to your reading list.')
    
    return render_template('reading_list.html', reading_list=reading_list.view_list())

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8525, debug=False)
