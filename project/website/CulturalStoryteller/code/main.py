from flask import Flask, render_template, request, redirect, url_for, session
import json
from user_manager import UserManager
from story_manager import StoryManager
from bookmark_manager import BookmarkManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.json')
story_manager = StoryManager('stories.json')
bookmark_manager = BookmarkManager('bookmarks.json')

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
        else:
            return render_template('registration.html', error="Username already exists.")
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    stories = story_manager.load_stories()
    return render_template('dashboard.html', stories=stories)

@app.route('/story/<title>', methods=['GET'])
def view_story_details(title):
    stories = story_manager.load_stories()
    story = next((s for s in stories if s.title == title), None)
    return render_template('story_details.html', story=story)

@app.route('/bookmarks', methods=['GET'])
def bookmarks():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = session['username']
    bookmarked_stories = bookmark_manager.load_bookmarks(user)
    return render_template('bookmarks.html', stories=bookmarked_stories)

@app.route('/login', methods=['POST'])
def user_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/bookmark', methods=['POST'])
def add_bookmark():
    if 'username' not in session:
        return redirect(url_for('login'))
    story_title = request.form['story_title']
    username = session['username']
    bookmark_manager.add_bookmark(username, story_title)
    return redirect(url_for('bookmarks'))

@app.route('/remove_bookmark', methods=['POST'])
def remove_bookmark():
    if 'username' not in session:
        return redirect(url_for('login'))
    story_title = request.form['story_title']
    username = session['username']
    bookmark_manager.remove_bookmark(username, story_title)
    return redirect(url_for('bookmarks'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search_for_stories():
    if request.method == 'POST':
        keyword = request.form['keyword']
        stories = story_manager.search_stories(keyword)
        return render_template('search_results.html', stories=stories)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(port=9015, debug=False)
