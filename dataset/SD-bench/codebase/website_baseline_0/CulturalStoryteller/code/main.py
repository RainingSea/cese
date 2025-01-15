from flask import Flask, render_template, request, redirect, url_for, session

from user_manager import UserManager
from story_manager import StoryManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
story_manager = StoryManager()

@app.route('/')
def login():
    """Render the login page."""
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Username already exists!"
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """Render the dashboard with stories and handle bookmarking."""
    if request.method == 'POST':
        username = session.get('username')
        bookmarks = request.form.getlist('bookmarks')
        story_manager.save_bookmarks(username, [int(story_id) for story_id in bookmarks])
    stories = story_manager.stories
    return render_template('dashboard.html', stories=stories)

@app.route('/story/<int:story_id>')
def story_details(story_id):
    """Render the details of a specific story."""
    story = story_manager.get_story_details(story_id)
    if not story:
        return "Story not found!", 404
    return render_template('story_details.html', story=story)

@app.route('/bookmarks')
def bookmarks():
    """Render the user's bookmarked stories."""
    username = session.get('username')
    bookmarks = story_manager.load_bookmarks(username)
    bookmarked_stories = [story_manager.get_story_details(story_id) for story_id in bookmarks]
    return render_template('bookmarks.html', stories=bookmarked_stories)

@app.route('/login', methods=['POST'])
def do_login():
    """Handle user login."""
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Invalid credentials!"

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('username', None)
    user_manager.logout()
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Handle story search functionality."""
    if request.method == 'POST':
        query = request.form['query']
        search_results = story_manager.search_stories(query)
        return render_template('search_results.html', stories=search_results)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(port=8528, debug=False)
