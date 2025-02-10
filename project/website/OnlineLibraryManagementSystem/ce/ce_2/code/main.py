from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from BookManager import BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
book_manager = BookManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = user_manager.get_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/book_management', methods=['GET', 'POST'])
def book_management():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        book_manager.add_book(Book(title, author, isbn))
    books = book_manager.get_books()
    return render_template('book_management.html', books=books)

@app.route('/user_management')
def user_management():
    users = user_manager.get_users()
    return render_template('user_management.html', users=users)

if __name__ == '__main__':
    user_manager.load_users()
    book_manager.load_books()
    app.run(port=8665, debug=False)
