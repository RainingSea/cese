from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from story_manager import StoryManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
story_manager = StoryManager('stories.txt', 'bookmarks.txt')

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
            return "User already exists!"
    return render_template('register.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' in session:
        stories = story_manager.stories
        return render_template('dashboard.html', stories=stories)
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Invalid credentials!"

@app.route('/story/<int:story_id>', methods=['GET'])
def story_details(story_id):
    story = story_manager.get_story_details(story_id)
    return render_template('story_details.html', story=story)

@app.route('/bookmarks', methods=['GET'])
def bookmarks():
    if 'username' in session:
        bookmarks = story_manager.load_bookmarks(session['username'])
        return render_template('bookmarks.html', bookmarks=bookmarks)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(port=8607, debug=False)
