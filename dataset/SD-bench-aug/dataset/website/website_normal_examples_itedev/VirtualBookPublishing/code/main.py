from flask import Flask, render_template, request, redirect, session, flash
from user_manager import UserManager
from book_manager import BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
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
            flash('Registration failed. Username may already exist.')
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    welcome_message = f"Welcome, {session['username']}!"
    return render_template('dashboard.html', username=session['username'], welcome_message=welcome_message)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    else:
        flash('Invalid username or password.')
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/create_book', methods=['GET', 'POST'])
def create_book():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        book_manager.add_book(title, author, content)
        flash('Book created successfully!')
        return redirect('/my_books')
    return render_template('create_book.html')

@app.route('/my_books')
def my_books():
    if 'username' not in session:
        return redirect('/')
    books = book_manager.get_books()
    return render_template('my_books.html', books=books)

@app.route('/book_details/<title>')
def book_details(title):
    if 'username' not in session:
        return redirect('/')
    book = book_manager.get_book_details(title)
    return render_template('book_details.html', book=book)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    user_manager.load_users()
    book_manager.load_books()
    app.run(debug=True)