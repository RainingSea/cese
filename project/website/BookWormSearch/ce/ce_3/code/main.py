from flask import Flask, render_template, request, redirect, session
from user import User
from book_manager import BookManager
from reading_list import ReadingList

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = User()
book_manager = BookManager()
reading_list_manager = ReadingList()

@app.route('/')
def login():
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
        search_results = book_manager.search_books(query)
        return render_template('dashboard.html', books=search_results)
    return render_template('dashboard.html', books=[])

@app.route('/book/<int:book_id>')
def book_details(book_id):
    book = book_manager.load_books()[book_id]
    return render_template('book_details.html', book=book)

@app.route('/reading_list')
def reading_list():
    user_reading_list = reading_list_manager.load_reading_list()
    return render_template('reading_list.html', books=user_reading_list)

if __name__ == '__main__':
    app.run(port=8995, debug=False)
