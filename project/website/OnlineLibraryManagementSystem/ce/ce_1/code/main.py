from flask import Flask, render_template, request, redirect, session, flash
from user_management import UserManager
from book_management import BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
book_manager = BookManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect('/')
        else:
            flash('Username already exists. Please choose another one.')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect('/')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    flash('Invalid username or password. Please try again.')
    return redirect('/')

@app.route('/logout')
def logout():
    user_manager.logout()
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect('/')

@app.route('/book_management', methods=['GET', 'POST'])
def book_management():
    if 'username' in session:
        if request.method == 'POST':
            title = request.form['title']
            author = request.form['author']
            year = int(request.form['year'])
            if book_manager.add_book(title, author, year):
                flash('Book added successfully.')
            else:
                flash('Failed to add book.')
        return render_template('book_management.html', books=book_manager.get_books())
    return redirect('/')

@app.route('/user_management')
def user_management():
    if 'username' in session:
        return render_template('user_management.html', users=user_manager.get_users())
    return redirect('/')

@app.route('/search_books', methods=['GET', 'POST'])
def search_books():
    if 'username' in session:
        if request.method == 'POST':
            query = request.form['query']
            results = book_manager.search_books(query)
            return render_template('search_books.html', results=results)
        return render_template('search_books.html')
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8481, debug=False)
