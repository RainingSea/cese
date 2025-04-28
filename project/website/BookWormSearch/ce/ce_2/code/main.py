from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from book_manager import BookManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
book_manager = BookManager()

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
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        query = request.form['query']
        results = book_manager.search_books(query)
        return render_template('dashboard.html', results=results)
    return render_template('dashboard.html')

@app.route('/book/<title>')
def book_details(title):
    details = book_manager.get_book_details(title)
    return render_template('book_details.html', details=details)

@app.route('/reading_list')
def reading_list():
    user_reading_list = user_manager.get_reading_list(session['username'])
    return render_template('reading_list.html', reading_list=user_reading_list)

if __name__ == '__main__':
    app.run(port=8301, debug=False)
