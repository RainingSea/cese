from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from book_manager import BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
user_manager = UserManager('users.txt')
book_manager = BookManager('books.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials, please try again."
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/book_management', methods=['GET', 'POST'])
def book_management():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        action = request.form['action']
        title = request.form['title']
        author = request.form['author']

        if action == 'add':
            book_manager.add_book(title, author)
        elif action == 'delete':
            book_manager.delete_book(title)

    books = book_manager.list_books()
    return render_template('book_management.html', books=books)

@app.route('/user_management', methods=['GET', 'POST'])
def user_management():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        action = request.form['action']
        username = request.form['username']
        password = request.form['password']

        if action == 'add':
            user_manager.register_user(username, password)

    users = user_manager.list_users()
    return render_template('user_management.html', users=users)

@app.route('/search_books', methods=['GET', 'POST'])
def search_books():
    if 'username' not in session:
        return redirect(url_for('login'))

    search_results = []
    if request.method == 'POST':
        query = request.form['query']
        search_results = book_manager.search_books(query)

    return render_template('search_books.html', results=search_results)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)