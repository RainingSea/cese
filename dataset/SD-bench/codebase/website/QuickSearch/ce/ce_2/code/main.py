from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from book_collection import BookCollection
from reading_list import ReadingList

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and books
user_manager = User()
book_manager = BookCollection()
book_manager.load_books('books.txt')

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
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        query = request.form['query']
        search_results = book_manager.search_books(query)
        return render_template('dashboard.html', books=search_results)
    return render_template('dashboard.html', books=[])

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/reading_list')
def reading_list():
    user_reading_list = ReadingList(session['username'])
    return render_template('reading_list.html', books=user_reading_list.get_reading_list())

if __name__ == '__main__':
    app.run(port=8682, debug=False)
