from flask import Flask, render_template, request, redirect, session, url_for
from user import User
from book import Book
from reading_list import ReadingList

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User()
        if user.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        search_query = request.form['search']
        # Logic to fetch books based on the search_query would go here
        # For now, we'll just return a placeholder list
        books = [{'title': 'Sample Book', 'author': 'Sample Author', 'summary': 'Sample Summary'}]
        return render_template('dashboard.html', books=books)

    return render_template('dashboard.html')

@app.route('/reading_list')
def reading_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    reading_list = ReadingList(username)
    books = reading_list.get_books()
    return render_template('reading_list.html', books=books)

@app.route('/book/<title>')
def book_details(title):
    # Logic to fetch book details would go here
    book = Book(title, "Sample Author", "Sample Summary")
    return render_template('book_details.html', book=book.get_details())

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User()
    if user.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8590, debug=False)
