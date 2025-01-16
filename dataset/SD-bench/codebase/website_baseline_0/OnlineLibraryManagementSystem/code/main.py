from flask import Flask, render_template, request, redirect, session
from UserManager import UserManager
from BookManager import BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

user_manager = UserManager('users.txt')
book_manager = BookManager('books.txt')

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
    return render_template('user_management.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect('/')

@app.route('/manage_books', methods=['GET', 'POST'])
def manage_books():
    if 'username' not in session:
        return redirect('/')
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        book_manager.add_book(title, author)
    
    books = book_manager.get_books()
    return render_template('book_management.html', books=books)

@app.route('/search_books', methods=['GET'])
def search_books():
    if 'username' not in session:
        return redirect('/')
    
    query = request.args.get('query', '')
    search_results = book_manager.search_books(query)
    books = book_manager.get_books()
    return render_template('book_management.html', books=books, search_results=search_results)

if __name__ == '__main__':
    app.run(port=8543, debug=False)
