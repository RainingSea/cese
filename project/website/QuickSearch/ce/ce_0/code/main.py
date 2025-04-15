from flask import Flask, render_template, request, redirect, session
from user import User
from book import BookManager
from reading_list import ReadingList

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and books at startup
users = User.load_users()
book_manager = BookManager()
books = book_manager.load_books()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register():
            return redirect('/')
        else:
            return render_template('registration.html', error="Username already taken.")
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        query = request.form['query']
        search_results = book_manager.search_books(query)
        return render_template('dashboard.html', books=search_results)
    return render_template('dashboard.html', books=[])

@app.route('/book/<title>', methods=['GET', 'POST'])
def book_details(title):
    book = book_manager.get_book_details(title)
    if request.method == 'POST':
        user = session.get('user')
        reading_list = ReadingList(user)
        if reading_list.add_book(book):
            return redirect('/reading_list')
    return render_template('book_details.html', book=book)

@app.route('/reading_list')
def reading_list():
    user = session.get('user')
    reading_list = ReadingList(user)
    return render_template('reading_list.html', books=reading_list.get_books())

if __name__ == '__main__':
    app.run(port=8321, debug=False)
