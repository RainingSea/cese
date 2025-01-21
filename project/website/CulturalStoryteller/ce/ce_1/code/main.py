from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from story_manager import StoryManager
from bookmark_manager import BookmarkManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
story_manager = StoryManager()
bookmark_manager = BookmarkManager()

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
            return "Username already exists!"
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    stories = story_manager.load_stories()
    return render_template('dashboard.html', stories=stories)

@app.route('/story/<title>', methods=['GET'])
def story_details(title):
    stories = story_manager.load_stories()
    story = next((s for s in stories if s.title == title), None)
    return render_template('story_details.html', story=story)

@app.route('/bookmarks', methods=['GET'])
def bookmarks():
    username = session.get('username')
    bookmarks = bookmark_manager.load_bookmarks(username)
    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Invalid credentials!"

if __name__ == '__main__':
    app.run(port=9011, debug=False)
