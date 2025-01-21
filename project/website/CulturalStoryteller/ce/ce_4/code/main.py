from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Story:
    def __init__(self, title: str, content: str, cultural_background: str):
        self.title = title
        self.content = content
        self.cultural_background = cultural_background

def load_users():
    users = []
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    return users

def load_stories():
    stories = []
    if os.path.exists('stories.txt'):
        with open('stories.txt', 'r') as f:
            for line in f:
                title, content, cultural_background = line.strip().split('|')
                stories.append(Story(title, content, cultural_background))
    return stories

def load_bookmarks():
    bookmarks = {}
    if os.path.exists('bookmarks.txt'):
        with open('bookmarks.txt', 'r') as f:
            for line in f:
                username, title = line.strip().split('|')
                if username in bookmarks:
                    bookmarks[username].append(title)
                else:
                    bookmarks[username] = [title]
    return bookmarks

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    stories = load_stories()
    return render_template('dashboard.html', stories=stories)

@app.route('/story/<title>')
def story_details(title):
    stories = load_stories()
    story = next((s for s in stories if s.title == title), None)
    return render_template('story_details.html', story=story)

@app.route('/bookmark/<title>', methods=['POST'])
def bookmark_story(title):
    username = session.get('username')
    if username:
        with open('bookmarks.txt', 'a') as f:
            f.write(f"{username}|{title}\n")
    return redirect(url_for('story_details', title=title))

@app.route('/bookmarks')
def bookmarks():
    username = session.get('username')
    bookmarks = load_bookmarks()
    user_bookmarks = bookmarks.get(username, [])
    return render_template('bookmarks.html', bookmarks=user_bookmarks)

if __name__ == '__main__':
    app.run(port=9014, debug=False)
