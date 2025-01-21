from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from culture import Culture
from bookmark import Bookmark

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users, cultures, and bookmarks from files
def load_users():
    user = User()
    return user.load_users()

def load_cultures():
    culture = Culture()
    return culture.load_cultures()

def load_bookmarks(username):
    bookmark = Bookmark(username)
    return bookmark.load_bookmarks(username)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    cultures = load_cultures()
    return render_template('dashboard.html', cultures=cultures)

@app.route('/culture/<name>')
def culture_details(name):
    culture = load_cultures()
    culture_info = next((c for c in culture if c.name == name), None)
    return render_template('culture_details.html', culture=culture_info)

@app.route('/bookmarks')
def bookmarks():
    username = session.get('username')
    bookmarks = load_bookmarks(username)
    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    if any(user.username == username and user.password == password for user in users):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=9019, debug=False)
