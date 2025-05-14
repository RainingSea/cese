from flask import Flask, render_template, request, redirect, url_for, session, flash
from LibrarySystem import LibrarySystem

app = Flask(__name__)
app.secret_key = 'secret_key_here'
library_system = LibrarySystem()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if library_system.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            library_system.user_manager.add_user(username, password)
            flash('Registration successful. Please login.')
            return redirect(url_for('login'))
        except ValueError as e:
            flash(str(e))
    return render_template('register.html')

@app.route('/logout')
def logout():
    library_system.logout()
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    stats = library_system.get_stats()
    return render_template('dashboard.html', stats=stats)

@app.route('/books', methods=['GET', 'POST'])
def books():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'add' in request.form:
            title = request.form['title']
            author = request.form['author']
            isbn = request.form['isbn']
            try:
                library_system.book_manager.add_book(title, author, isbn)
                flash('Book added successfully')
            except ValueError as e:
                flash(str(e))
        elif 'delete' in request.form:
            isbn = request.form['isbn']
            try:
                library_system.book_manager.delete_book(isbn)
                flash('Book deleted successfully')
            except ValueError as e:
                flash(str(e))
    
    book_list = library_system.book_manager.list_books()
    return render_template('books.html', books=book_list)

@app.route('/users', methods=['GET', 'POST'])
def users():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            library_system.user_manager.add_user(username, password)
            flash('User added successfully')
        except ValueError as e:
            flash(str(e))
    
    user_list = library_system.user_manager.list_users()
    return render_template('users.html', users=user_list)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    results = []
    if request.method == 'POST':
        query = request.form['query']
        results = library_system.book_manager.search_books(query)
    
    return render_template('search.html', results=results)

if __name__ == '__main__':
    app.run(port=8112, debug=False)
