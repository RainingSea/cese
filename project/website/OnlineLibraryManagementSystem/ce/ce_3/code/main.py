from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from book_manager import BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
book_manager = BookManager('books.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/book_management', methods=['GET', 'POST'])
def book_management():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        if request.form['action'] == 'Add':
            book_manager.add_book(title, author)
        elif request.form['action'] == 'Delete':
            book_manager.delete_book(title)
    books = book_manager.get_books()
    return render_template('book_management.html', books=books)

@app.route('/user_management')
def user_management():
    users = user_manager.get_users()
    return render_template('user_management.html', users=users)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        results = book_manager.search_books(query)
        return render_template('search.html', results=results)
    return render_template('search.html', results=[])

if __name__ == '__main__':
    app.run(port=8666, debug=False)
