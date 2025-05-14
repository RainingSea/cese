from flask import Flask, render_template, request, redirect, url_for, session
from library import LibrarySystem

app = Flask(__name__)
app.secret_key = 'secret_key'
library = LibrarySystem()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if library.authenticate_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/books', methods=['GET', 'POST'])
def book_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'add_book' in request.form:
            title = request.form['title']
            author = request.form['author']
            isbn = request.form['isbn']
            library.add_book(title, author, isbn)
        elif 'delete_book' in request.form:
            isbn = request.form['isbn']
            library.delete_book(isbn)
    
    books = library.list_books()
    return render_template('books.html', books=books)

@app.route('/users', methods=['GET', 'POST'])
def user_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        library.register_user(username, password, role)
    
    users = library.list_users()
    return render_template('users.html', users=users)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    results = []
    if request.method == 'POST':
        query = request.form['query']
        results = library.search_books(query)
    
    return render_template('search.html', results=results)

if __name__ == '__main__':
    app.run(port=8105, debug=False)
