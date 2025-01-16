from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from book_manager import BookManager
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for session management

class App:
    def __init__(self, user_file: str, book_file: str):
        self.user_manager = UserManager(user_file)
        self.book_manager = BookManager(book_file)

    def run(self) -> None:
        app.run(port=8694, debug=False)

    @app.route('/', methods=['GET', 'POST'])
    def login_user():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if self.user_manager.login(username, password):
                session['username'] = username  # Store username in session
                return redirect(url_for('dashboard'))
            else:
                return "Login failed. Please check your credentials."
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register_user():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if self.user_manager.register(username, password):
                return redirect(url_for('login_user'))
            else:
                return "Registration failed. Username may already exist."
        return render_template('registration.html')

    @app.route('/dashboard')
    def dashboard():
        if 'username' not in session:
            return redirect(url_for('login_user'))  # Ensure user is logged in
        time.sleep(1)  # Simulate loading delay
        return render_template('dashboard.html')

    @app.route('/create_book', methods=['GET', 'POST'])
    def create_new_book():
        if 'username' not in session:
            return redirect(url_for('login_user'))  # Ensure user is logged in
        if request.method == 'POST':
            title = request.form['title']
            author = request.form['author']
            content = request.form['content']
            if self.book_manager.create_book(title, author, content):
                return redirect(url_for('view_my_books'))
            else:
                return "Failed to create book."
        return render_template('create_book.html')

    @app.route('/my_books')
    def view_my_books():
        if 'username' not in session:
            return redirect(url_for('login_user'))  # Ensure user is logged in
        time.sleep(1)  # Simulate loading delay
        books = self.book_manager.get_books()
        return render_template('my_books.html', books=books)

    @app.route('/book/<title>')
    def view_book_details(title):
        if 'username' not in session:
            return redirect(url_for('login_user'))  # Ensure user is logged in
        time.sleep(1)  # Simulate loading delay
        book_details = self.book_manager.get_book_details(title)
        return render_template('book_details.html', book=book_details)

    @app.route('/about')
    def about():
        return render_template('about.html')

if __name__ == '__main__':
    app_instance = App('users.txt', 'books.txt')
    app_instance.run()