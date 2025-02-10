from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from culture_manager import CultureManager
from bookmark_manager import BookmarkManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'

user_manager = UserManager('users.txt')
culture_manager = CultureManager('cultures.txt')
bookmark_manager = BookmarkManager('bookmarks.txt')

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
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    cultures = culture_manager.load_cultures()
    return render_template('dashboard.html', cultures=cultures)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/bookmarks')
def bookmarks():
    if 'username' in session:
        bookmarks = bookmark_manager.load_bookmarks(session['username'])
        return render_template('bookmarks.html', bookmarks=bookmarks)
    return redirect(url_for('login'))

@app.route('/culture/<culture_name>')
def culture_details(culture_name):
    details = culture_manager.get_culture_details(culture_name)
    return render_template('culture_details.html', details=details)

if __name__ == '__main__':
    app.run(port=8613, debug=False)
