from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from BookManager import BookManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Used for session management

user_manager = UserManager('users.txt')
book_manager = BookManager('books.txt', 'reading_list.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        query = request.form['query']
        books = book_manager.search_books(query)
        return render_template('dashboard.html', books=books)
    
    return render_template('dashboard.html')

@app.route('/book/<int:book_id>')
def book_details(book_id):
    book = book_manager.load_books()[book_id]  # Assuming book_id corresponds to index
    return render_template('book_details.html', book=book)

@app.route('/reading_list')
def reading_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    reading_list = book_manager.get_reading_list(session['username'])
    return render_template('reading_list.html', reading_list=reading_list)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8591, debug=False)
