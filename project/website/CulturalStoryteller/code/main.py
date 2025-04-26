from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_session import Session

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in [user.split('|')[0] for user in self.users]:
            return False
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        self.users.append(f"{username}|{password}")
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user == f"{username}|{password}" for user in self.users)

    def load_users(self) -> list:
        try:
            with open('users.txt', 'r') as f:
                return f.read().strip().split('\n')
        except FileNotFoundError:
            return []

class StoryManager:
    def __init__(self):
        self.stories = self.load_stories()

    def load_stories(self) -> list:
        try:
            with open('stories.txt', 'r') as f:
                return f.read().strip().split('\n')
        except FileNotFoundError:
            return []

    def search_stories(self, keyword: str) -> list:
        return [story for story in self.stories if keyword.lower() in story.lower()]

    def get_story_details(self, story_id: int) -> str:
        return self.stories[story_id] if 0 <= story_id < len(self.stories) else "Story not found."

class BookmarkManager:
    def __init__(self):
        self.bookmarks = self.load_bookmarks()

    def add_bookmark(self, story_id: str) -> bool:
        if story_id in self.bookmarks:
            return False
        self.bookmarks.append(story_id)
        self.save_bookmarks()
        return True

    def remove_bookmark(self, story_id: str) -> bool:
        if story_id in self.bookmarks:
            self.bookmarks.remove(story_id)
            self.save_bookmarks()
            return True
        return False

    def load_bookmarks(self) -> list:
        try:
            with open('bookmarks.txt', 'r') as f:
                return f.read().strip().split('\n')
        except FileNotFoundError:
            return []

    def save_bookmarks(self):
        with open('bookmarks.txt', 'w') as f:
            f.write('\n'.join(self.bookmarks))

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'supersecretkey'  # Needed for session management
Session(app)

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
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        flash("Registration failed. Username may already exist.", "error")
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    stories = story_manager.load_stories()
    return render_template('dashboard.html', stories=stories)

@app.route('/story/<int:story_id>')
def story_details(story_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    story = story_manager.get_story_details(story_id)
    return render_template('story_details.html', story=story)

@app.route('/bookmarks', methods=['GET', 'POST'])
def bookmarks():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        story_id = request.form['story_id']
        if bookmark_manager.add_bookmark(story_id):
            flash("Story added to bookmarks.", "success")
        else:
            flash("Story already in bookmarks.", "error")
    return render_template('bookmarks.html', bookmarks=bookmark_manager.bookmarks)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    flash("Invalid credentials. Please try again.", "error")
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8146, debug=False)
