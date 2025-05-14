from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class BookManager:
    def __init__(self, books_file='books.txt'):
        self.books_file = books_file

    def add_book(self, title, author, isbn):
        try:
            with open(self.books_file, 'a') as f:
                f.write(f"{title},{author},{isbn}\n")
            return True
        except:
            return False

    def delete_book(self, isbn):
        try:
            with open(self.books_file, 'r') as f:
                books = [line.strip().split(',') for line in f.readlines()]
            
            with open(self.books_file, 'w') as f:
                for book in books:
                    if book[2] != isbn:
                        f.write(','.join(book) + '\n')
            return True
        except:
            return False

    def list_books(self):
        try:
            with open(self.books_file, 'r') as f:
                return [line.strip().split(',') for line in f.readlines()]
        except:
            return []

    def search_books(self, query):
        books = self.list_books()
        return [book for book in books if query.lower() in book[0].lower() or query.lower() in book[1].lower()]

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file

    def add_user(self, username, password):
        try:
            with open(self.users_file, 'a') as f:
                f.write(f"{username},{password}\n")
            return True
        except:
            return False

    def list_users(self):
        try:
            with open(self.users_file, 'r') as f:
                return [line.strip().split(',') for line in f.readlines()]
        except:
            return []

    def validate_user(self, username, password):
        users = self.list_users()
        for user in users:
            if user[0] == username and user[1] == password:
                return True
        return False

book_manager = BookManager()
user_manager = UserManager()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.validate_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if user_manager.add_user(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return render_template('login.html', error="Registration failed")

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    books = book_manager.list_books()
    users = user_manager.list_users()
    return render_template('dashboard.html', 
                          username=session['username'],
                          book_count=len(books),
                          user_count=len(users))

@app.route('/books', methods=['GET', 'POST'])
def books():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        book_manager.add_book(title, author, isbn)
    
    book_list = book_manager.list_books()
    return render_template('books.html', books=book_list)

@app.route('/delete_book/<isbn>')
def delete_book(isbn):
    if 'username' not in session:
        return redirect(url_for('login'))
    book_manager.delete_book(isbn)
    return redirect(url_for('books'))

@app.route('/users')
def users():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.add_user(username, password)
    
    user_list = user_manager.list_users()
    return render_template('users.html', users=user_list)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    results = []
    if request.method == 'POST':
        query = request.form['query']
        results = book_manager.search_books(query)
    
    return render_template('search.html', results=results)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8107, debug=False)
