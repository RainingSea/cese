from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from StoryManager import StoryManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

user_manager = UserManager()
story_manager = StoryManager()

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
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    stories = story_manager.stories
    return render_template('dashboard.html', stories=stories)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/story/<title>')
def story_details(title):
    story = next((s for s in story_manager.stories if s['title'] == title), None)
    return render_template('story_details.html', story=story)

@app.route('/bookmarks')
def bookmarks():
    if 'username' in session:
        bookmarks = story_manager.get_bookmarks(session['username'])
        return render_template('bookmarks.html', bookmarks=bookmarks)
    return redirect(url_for('login'))

if __name__ == '__main__':
    user_manager.load_users()
    story_manager.load_stories()
    app.run(port=8308, debug=False)
