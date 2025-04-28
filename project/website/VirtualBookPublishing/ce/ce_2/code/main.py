from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from book_manager import BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

user_manager = UserManager('users.txt')
book_manager = BookManager('books.txt')

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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/create_book', methods=['GET', 'POST'])
def create_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        username = session.get('username')  # Assuming user is logged in
        book_manager.create_book(username, title, author, content)
        return redirect(url_for('my_books'))
    return render_template('create_book.html')

@app.route('/my_books')
def my_books():
    username = session.get('username')  # Assuming user is logged in
    books = book_manager.get_books(username)
    return render_template('my_books.html', books=books)

@app.route('/book_details/<title>')
def book_details(title):
    details = book_manager.get_book_details(title)
    return render_template('book_details.html', details=details)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=8456, debug=False)
