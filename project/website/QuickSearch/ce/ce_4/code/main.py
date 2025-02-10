from flask import Flask, render_template, request, redirect, session
from user import User
from book import Book
from reading_list import ReadingList

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and books data
user_data = User.load_users()
book_data = Book.load_books()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User()
        if user.register(username, password):
            return redirect('/')
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/')
    
    if request.method == 'POST':
        query = request.form['query']
        books = Book.search_books(query)
    else:
        books = book_data

    return render_template('dashboard.html', books=books)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User()
    if user.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return redirect('/')

@app.route('/book/<title>')
def book_details(title):
    book = next((book for book in book_data if book.title == title), None)
    return render_template('book_details.html', book=book)

@app.route('/reading_list')
def reading_list():
    if 'username' not in session:
        return redirect('/')
    
    reading_list = ReadingList.load_reading_list(session['username'])
    return render_template('reading_list.html', reading_list=reading_list)

if __name__ == '__main__':
    app.run(port=8684, debug=False)
