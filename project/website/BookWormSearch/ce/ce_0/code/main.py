from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from reading_list import ReadingList
from book_manager import BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and books
users = User.load_users('users.txt')
reading_lists = {}
books = BookManager()
books.load_books('books.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register(users):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        query = request.form['query']
        search_results = books.search_books(query)
        return render_template('dashboard.html', books=search_results)
    return render_template('dashboard.html', books=[])

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    if user.login(users):
        session['username'] = username
        reading_lists[username] = ReadingList(user)
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/book/<title>')
def book_details(title):
    book = books.get_book(title)
    return render_template('book_details.html', book=book)

@app.route('/add_to_reading_list/<title>')
def add_to_reading_list(title):
    if 'username' in session:
        reading_lists[session['username']].add_book(books.get_book(title))
    return redirect(url_for('dashboard'))

@app.route('/reading_list')
def reading_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_reading_list = reading_lists[session['username']].get_books()
    return render_template('reading_list.html', books=user_reading_list)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8992, debug=False)
