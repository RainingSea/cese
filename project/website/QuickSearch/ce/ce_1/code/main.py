from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users[username] = password
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class SearchEngine:
    def __init__(self):
        self.books = self.load_books()

    def load_books(self):
        books = []
        with open('books.json', 'r') as f:
            books = json.load(f)
        return books

    def search(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book['title'].lower()]

    def get_book_details(self, book_id: str) -> dict:
        for book in self.books:
            if book['id'] == book_id:
                return book
        return {}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
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
    if request.method == 'POST':
        query = request.form['query']
        results = search_engine.search(query)
        return render_template('dashboard.html', results=results)
    return render_template('dashboard.html', results=[])

@app.route('/book/<book_id>')
def book_details(book_id):
    book = search_engine.get_book_details(book_id)
    return render_template('book_details.html', book=book)

@app.route('/reading_list')
def reading_list():
    # Placeholder for reading list functionality
    return render_template('reading_list.html')

if __name__ == '__main__':
    user_manager = UserManager()
    search_engine = SearchEngine()
    app.run(port=8227, debug=False)
