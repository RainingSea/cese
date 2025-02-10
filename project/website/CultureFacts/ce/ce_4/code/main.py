from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from culture import Culture
from bookmark_manager import BookmarkManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users

def load_cultures():
    cultures = {}
    with open('cultures.txt', 'r') as file:
        for line in file:
            name, facts = line.strip().split('|')
            cultures[name] = Culture(name, facts.split(','))
    return cultures

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.save_user():
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    cultures = load_cultures()
    return render_template('dashboard.html', cultures=cultures)

@app.route('/culture/<name>')
def culture_details(name):
    cultures = load_cultures()
    culture = cultures.get(name)
    return render_template('culture_details.html', culture=culture)

@app.route('/bookmarks')
def bookmarks():
    username = session.get('username')
    bookmark_manager = BookmarkManager(username)
    bookmarks = bookmark_manager.get_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8615, debug=False)
