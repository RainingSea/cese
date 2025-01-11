from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from StoryManager import StoryManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
story_manager = StoryManager('stories.txt')

@app.route('/')
def login():
    """Renders the login page."""
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('story_creation'))
    return render_template('login.html', error="Invalid credentials")

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
        return render_template('register.html', error="Username already exists")
    return render_template('register.html')

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation():
    """Handles story creation and displays existing stories."""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        username = session.get('username')
        if title and content:
            story_manager.save_story(username, title, content)
            return redirect(url_for('story_creation'))
    return render_template('story_creation.html', stories=story_manager.stories)

@app.route('/edit_story/<title>', methods=['GET', 'POST'])
def edit_story(title):
    """Handles story editing."""
    username = session.get('username')
    if request.method == 'POST':
        new_content = request.form['content']
        if story_manager.edit_story(username, title, new_content):
            return redirect(url_for('story_creation'))
        return render_template('edit_story.html', title=title, error="Failed to edit story")
    return render_template('edit_story.html', title=title)

@app.route('/logout')
def logout():
    """Handles user logout."""
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8366, debug=False)
