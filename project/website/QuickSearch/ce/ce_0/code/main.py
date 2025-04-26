from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from tools import UserManager, BookManager, ReadingList

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

user_manager = UserManager()
book_manager = BookManager()
reading_list_manager = ReadingList()

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
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        query = request.form['query']
        results = book_manager.search_books(query)
        return render_template('dashboard.html', results=results)
    return render_template('dashboard.html')

@app.route('/book/<int:book_id>')
def book_details(book_id):
    if 'username' not in session:
        return redirect('/')
    book = book_manager.books[book_id]
    return render_template('book_details.html', book=book)

@app.route('/reading_list')
def reading_list():
    if 'username' not in session:
        return redirect('/')
    user_reading_list = reading_list_manager.reading_list.get(session['username'], [])
    return render_template('reading_list.html', reading_list=user_reading_list)

if __name__ == '__main__':
    user_manager.load_users()
    book_manager.load_books()
    reading_list_manager.load_reading_list()
    app.run(port=8226, debug=False)
