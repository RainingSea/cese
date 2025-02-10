from flask import Flask, render_template, request, redirect, session, url_for
from user import User
from story import Story
from bookmark import Bookmark

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load data from files
def load_users():
    users = []
    with open('users.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_stories():
    stories = []
    with open('stories.txt', 'r') as f:
        for line in f:
            title, content, cultural_origin, category = line.strip().split('|')
            stories.append(Story(title, content, cultural_origin, category))
    return stories

def load_bookmarks():
    bookmarks = {}
    with open('bookmarks.txt', 'r') as f:
        for line in f:
            username, story_title = line.strip().split('|')
            if username in bookmarks:
                bookmarks[username].append(story_title)
            else:
                bookmarks[username] = [story_title]
    return bookmarks

users = load_users()
stories = load_stories()
bookmarks = load_bookmarks()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        users.append(new_user)
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', stories=stories)

@app.route('/story/<title>')
def story_details(title):
    story = next((s for s in stories if s.title == title), None)
    return render_template('story_details.html', story=story)

@app.route('/bookmarks')
def bookmarks_page():
    user_bookmarks = bookmarks.get(session.get('username', ''), [])
    return render_template('bookmarks.html', bookmarks=user_bookmarks)

@app.route('/add_bookmark/<title>')
def add_bookmark(title):
    if 'username' in session:
        username = session['username']
        if username not in bookmarks:
            bookmarks[username] = []
        bookmarks[username].append(title)
        with open('bookmarks.txt', 'a') as f:
            f.write(f"{username}|{title}\n")
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = next((u for u in users if u.username == username and u.password == password), None)
    if user:
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8606, debug=False)
