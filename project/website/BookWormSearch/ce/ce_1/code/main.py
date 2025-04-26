from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class BookManager:
    def __init__(self):
        self.books = self.load_books()

    def load_books(self):
        books = []
        if os.path.exists('books.txt'):
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author, genre = line.strip().split('|')
                    books.append({'title': title, 'author': author, 'genre': genre})
        return books

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book['title'].lower()]

    def get_book_details(self, title: str) -> dict:
        for book in self.books:
            if book['title'].lower() == title.lower():
                return book
        return {}

class ReadingList:
    def __init__(self, username: str):
        self.username = username
        self.reading_list = self.load_reading_list()

    def load_reading_list(self):
        reading_list = []
        filename = f"{self.username}_reading_list.txt"
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                for line in file:
                    title = line.strip()
                    reading_list.append(title)
        return reading_list

    def add_to_reading_list(self, book: dict) -> None:
        self.reading_list.append(book['title'])
        with open(f"{self.username}_reading_list.txt", 'a') as file:
            file.write(f"{book['title']}\n")

    def get_reading_list(self) -> list:
        return self.reading_list

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    user_manager = UserManager()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
        else:
            return "Username already exists!"
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user_manager = UserManager()
    book_manager = BookManager()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return render_template('dashboard.html', books=book_manager.books)
        else:
            return "Invalid credentials!"
    return render_template('login.html')

@app.route('/book/<title>')
def book_details(title):
    book_manager = BookManager()
    book = book_manager.get_book_details(title)
    return render_template('book_details.html', book=book)

@app.route('/reading_list')
def reading_list():
    if 'username' in session:
        reading_list_manager = ReadingList(session['username'])
        return render_template('reading_list.html', reading_list=reading_list_manager.get_reading_list())
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8292, debug=False)
