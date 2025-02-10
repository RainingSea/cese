from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from book import Book
from reading_list import ReadingList

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = User()
book_manager = Book()

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
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return render_template('dashboard.html', books=book_manager.load_books())
    return render_template('dashboard.html')

@app.route('/book/<title>')
def book_details(title):
    books = book_manager.load_books()
    book = next((b for b in books if b['title'] == title), None)
    return render_template('book_details.html', book=book)

@app.route('/reading_list')
def reading_list():
    username = session.get('username')
    reading_list_manager = ReadingList(username)
    books = reading_list_manager.load_reading_list()
    return render_template('reading_list.html', books=books)

if __name__ == '__main__':
    app.run(port=8587, debug=False)
