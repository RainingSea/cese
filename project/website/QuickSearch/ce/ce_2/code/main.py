from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

class UserManager:
    def __init__(self, filename):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users.append([username, password])
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)

class BookManager:
    def __init__(self, filename):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def search_books(self, query: str):
        return [book for book in self.books if query.lower() in book[0].lower()]

class ReadingList:
    def __init__(self, filename):
        self.filename = filename

    def load_reading_list(self, username: str):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as file:
            for line in file:
                if line.startswith(username):
                    return line.strip().split('|')[1:]
        return []

    def add_to_reading_list(self, username: str, book_title: str) -> bool:
        reading_list = self.load_reading_list(username)
        if book_title in reading_list:
            return False
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{book_title}\n")
        return True

user_manager = UserManager('users.txt')
book_manager = BookManager('books.txt')
reading_list_manager = ReadingList('reading_list.txt')

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
        else:
            return "User already exists!"
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return render_template('dashboard.html', books=book_manager.books)
        else:
            return "Invalid credentials!"
    return render_template('dashboard.html', books=book_manager.books)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    book = book_manager.books[book_id]
    return render_template('book_details.html', book=book)

@app.route('/reading_list')
def reading_list():
    if 'username' in session:
        user_reading_list = reading_list_manager.load_reading_list(session['username'])
        return render_template('reading_list.html', reading_list=user_reading_list)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8400, debug=False)
