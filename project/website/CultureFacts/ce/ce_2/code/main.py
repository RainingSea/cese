from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from culture import Culture
from bookmark import Bookmark

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_cultures():
    cultures = []
    with open('cultures.txt', 'r') as file:
        for line in file:
            name, facts = line.strip().split('|')
            cultures.append(Culture(name, facts))
    return cultures

def load_bookmarks(username):
    bookmarks = []
    with open('bookmarks.txt', 'r') as file:
        for line in file:
            user, culture_name = line.strip().split('|')
            if user == username:
                bookmarks.append(Bookmark(user, culture_name))
    return bookmarks

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
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    cultures = load_cultures()
    return render_template('dashboard.html', cultures=cultures)

@app.route('/culture/<name>')
def culture_details(name):
    cultures = load_cultures()
    culture = next((c for c in cultures if c.name == name), None)
    return render_template('culture_details.html', culture=culture)

@app.route('/bookmarks')
def bookmarks():
    username = session.get('username')
    bookmarks = load_bookmarks(username)
    return render_template('bookmarks.html', bookmarks=bookmarks)

if __name__ == '__main__':
    app.run(port=9018, debug=False)
