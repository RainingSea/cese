from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from story import Story
from bookmark import Bookmark
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
                title, content, cultural_origin = line.strip().split('|')
                stories.append(Story(title, content, cultural_origin))
    return stories

def load_bookmarks(username):
    bookmarks = []
    if os.path.exists('bookmarks.txt'):
        with open('bookmarks.txt', 'r') as f:
            for line in f:
                user, story_title = line.strip().split('|')
                if user == username:
                    bookmarks.append(story_title)
    return bookmarks

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    stories = load_stories()
    return render_template('dashboard.html', stories=stories)

@app.route('/story/<title>')
def view_story(title):
    stories = load_stories()
    story = next((s for s in stories if s.title == title), None)
    return render_template('story_details.html', story=story)

@app.route('/bookmarks')
def bookmarks():
    username = session.get('username')
    bookmarked_stories = load_bookmarks(username)
    return render_template('bookmarks.html', bookmarks=bookmarked_stories)

if __name__ == '__main__':
    app.run(port=8605, debug=False)
