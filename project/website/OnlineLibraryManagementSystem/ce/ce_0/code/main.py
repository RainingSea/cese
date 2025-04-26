from flask import Flask, render_template, request, redirect, session
from tools import UserManager, BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
book_manager = BookManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect('/dashboard')
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/book_management', methods=['GET', 'POST'])
def book_management():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        book_manager.add_book(title, author)
    books = book_manager.view_books()
    return render_template('book_management.html', books=books)

@app.route('/user_management', methods=['GET', 'POST'])
def user_management():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.register(username, password)
    users = user_manager.load_users()
    return render_template('user_management.html', users=users)

if __name__ == '__main__':
    user_manager.load_users()
    book_manager.load_books()
    app.run(port=8202, debug=False)
