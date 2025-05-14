from flask import Flask, render_template, request, redirect, url_for, session
from library import LibrarySystem

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
library = LibrarySystem()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if library.authenticate(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if library.register_user(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error="Registration failed (user may exist)")

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/books', methods=['GET', 'POST'])
def books():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'delete_isbn' in request.form:
            library.delete_book(request.form['delete_isbn'])
        else:
            title = request.form['title']
            author = request.form['author']
            isbn = request.form['isbn']
            library.add_book(title, author, isbn)
    
    book_list = library.list_books()
    return render_template('books.html', books=book_list)

@app.route('/users')
def users():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_list = library.list_users()
    return render_template('users.html', users=user_list)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    results = []
    if request.method == 'POST':
        query = request.form['query']
        results = library.search_books(query)
    
    return render_template('search.html', results=results)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8108, debug=False)
