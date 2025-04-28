from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from BookManager import BookManager
from ReadingList import ReadingList

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
book_manager = BookManager()
reading_list_manager = ReadingList()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.register(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        query = request.form['query']
        books = book_manager.search_books(query)
        return render_template('dashboard.html', books=books)
    return render_template('dashboard.html')

@app.route('/book/<book_id>')
def book_details(book_id):
    book = book_manager.books[int(book_id)]
    return render_template('book_details.html', book=book)

@app.route('/reading_list')
def reading_list():
    user_reading_list = reading_list_manager.get_reading_list(session.get('username', ''))
    return render_template('reading_list.html', reading_list=user_reading_list)

@app.route('/add_to_reading_list/<book_id>')
def add_to_reading_list(book_id):
    reading_list_manager.add_to_reading_list(session.get('username', ''), book_id)
    return redirect(url_for('reading_list'))

if __name__ == '__main__':
    user_manager.load_users()
    book_manager.load_books()
    reading_list_manager.load_reading_list()
    app.run(port=8300, debug=False)
