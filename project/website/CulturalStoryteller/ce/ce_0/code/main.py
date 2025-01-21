from flask import Flask, render_template, request, redirect, session
from user import User
from story import Story
from bookmark import Bookmark

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load data from files
def load_users():
    users = {}
    with open('users.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split('|')
            users[username] = password
    return users

def load_stories():
    stories = []
    with open('stories.txt', 'r') as f:
        for line in f:
            title, content, cultural_background = line.strip().split('|')
            stories.append(Story(title, content, cultural_background))
    return stories

def load_bookmarks():
    bookmarks = {}
    with open('bookmarks.txt', 'r') as f:
        for line in f:
            username, story_title = line.strip().split('|')
            if username not in bookmarks:
                bookmarks[username] = []
            bookmarks[username].append(story_title)
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
        user = User()
        if user.register(username, password):
            return redirect('/')
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

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User()
    if user.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=9010, debug=False)
