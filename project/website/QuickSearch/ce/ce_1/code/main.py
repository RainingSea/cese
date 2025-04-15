from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from book_manager import BookManager
from reading_list import ReadingList

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

user_manager = UserManager('users.txt')
book_manager = BookManager('books.txt')
reading_list_manager = ReadingList('reading_list.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username  # Store username in session
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return render_template('registration.html', error='Username already exists')
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        query = request.form['search']
        results = book_manager.search_books(query)
        return render_template('dashboard.html', results=results)
    return render_template('dashboard.html')

@app.route('/book/<title>', methods=['GET', 'POST'])
def book_details(title):
    if 'username' not in session:
        return redirect(url_for('login'))

    book = book_manager.get_book_details(title)
    if request.method == 'POST':
        reading_list_manager.add_to_reading_list(session['username'], title)
        return redirect(url_for('reading_list'))

    return render_template('book_details.html', book=book)

@app.route('/reading_list')
def reading_list():
    if 'username' not in session:
        return redirect(url_for('login'))

    books = reading_list_manager.get_reading_list(session['username'])
    return render_template('reading_list.html', books=books)

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8323, debug=False)
