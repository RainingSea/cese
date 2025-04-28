from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
from user_auth import UserAuth
from book_search import BookSearch
from reading_list import ReadingList

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

user_auth = UserAuth('users.txt')
book_search = BookSearch('books.txt')
reading_list = ReadingList('reading_list.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_auth.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        query = request.form['query']
        results = book_search.search_books(query)
        return render_template('dashboard.html', results=results)
    return render_template('dashboard.html', results=[])

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_auth.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/book/<title>')
def book_details(title):
    book_info = book_search.get_book_details(title)
    return render_template('book_details.html', book=book_info)

@app.route('/add_to_reading_list/<title>')
def add_to_reading_list(title):
    username = session.get('username')
    if username:
        reading_list.add_to_reading_list(username, title)
    return redirect(url_for('dashboard'))

@app.route('/reading_list')
def view_reading_list():
    username = session.get('username')
    books = reading_list.get_reading_list(username)
    return render_template('reading_list.html', books=books)

if __name__ == '__main__':
    app.run(port=8299, debug=False)
