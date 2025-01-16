from flask import Flask, render_template, request, redirect, session
from user import User
from book import Book
from reading_list import ReadingList
from data_storage import DataStorage

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

data_storage = DataStorage()
data_storage.load_users()  # Load users at startup
data_storage.load_books()  # Load books at startup

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        data_storage.save_user(user)
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.login(username, password):
            session['username'] = username
            return render_template('dashboard.html', books=data_storage.load_books())
    if 'username' in session:
        return render_template('dashboard.html', books=data_storage.load_books())
    return redirect('/')

@app.route('/book/<title>', methods=['GET'])
def book_details(title):
    books = data_storage.load_books()
    book = next((b for b in books if b.title == title), None)
    if book is None:
        return redirect('/dashboard')  # Redirect if book not found
    return render_template('book_details.html', book=book)

@app.route('/reading_list', methods=['GET'])
def reading_list():
    if 'username' in session:
        user_reading_list = ReadingList(session['username'])
        user_reading_list.books = data_storage.load_reading_list(session['username'])
        return render_template('reading_list.html', books=user_reading_list.get_books())
    return redirect('/')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8549, debug=False)
