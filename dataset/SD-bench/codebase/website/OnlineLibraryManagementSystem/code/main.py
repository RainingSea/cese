from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from book_manager import BookManager
from session_manager import SessionManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
book_manager = BookManager()
session_manager = SessionManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if session_manager.login(username, password):
            return redirect('/dashboard')
        return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.add_user(username, password):
            return redirect('/')
        return 'Username already exists', 400
    return render_template('register.html')

@app.route('/logout')
def logout():
    session_manager.logout()
    return redirect('/')

@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        action = request.form['action']
        username = request.form['username']
        if action == 'deactivate':
            user_manager.deactivate_user(username)
        elif action == 'change_password':
            new_password = request.form['new_password']
            user_manager.change_password(username, new_password)
    users = user_manager.get_users()
    return render_template('manage_users.html', users=users)

@app.route('/search_books', methods=['GET'])
def search_books():
    query = request.args.get('query', '')
    results = book_manager.search_books(query)
    return render_template('search_results.html', results=results)

if __name__ == '__main__':
    user_manager.load_users()
    book_manager.load_books()
    app.run(port=8668, debug=False)
