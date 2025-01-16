from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from BookManager import BookManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'

user_manager = UserManager()
book_manager = BookManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = user_manager.get_users()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    return 'Invalid credentials', 401

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/books')
def book_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    books = book_manager.get_books()
    return render_template('book_management.html', books=books)

@app.route('/users')
def user_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    users = user_manager.get_users()
    return render_template('user_management.html', users=users)

if __name__ == '__main__':
    app.run(port=8664, debug=False)
