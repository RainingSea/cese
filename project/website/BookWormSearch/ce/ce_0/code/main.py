from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from book_manager import BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key in production

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
            return redirect('/')
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        query = request.form['query']
        books = book_manager.search_books(query)
        return render_template('dashboard.html', books=books)
    return render_template('dashboard.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return redirect('/')

@app.route('/book/<book_id>')
def book_details(book_id):
    book = book_manager.books[int(book_id)]
    return render_template('book_details.html', book=book)

@app.route('/reading_list')
def reading_list():
    if 'username' not in session:
        return redirect('/')
    reading_list = user_manager.load_reading_list(session['username'])
    return render_template('reading_list.html', reading_list=reading_list)

if __name__ == '__main__':
    user_manager.load_users()
    book_manager.load_books()
    app.run(port=8291, debug=False)
