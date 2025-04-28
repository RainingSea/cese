from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_session import Session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)

class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def register(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password, 'bookmarks': []})
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                session['user_id'] = username
                return True
        return False

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append({'username': username, 'password': password, 'bookmarks': []})

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user['username']}|{user['password']}\n")

class StoryManager:
    def __init__(self):
        self.stories = []
        self.load_stories()

    def load_stories(self) -> None:
        if os.path.exists('stories.txt'):
            with open('stories.txt', 'r') as file:
                for line in file:
                    self.stories.append(line.strip())

    def get_story_details(self, story_id: int) -> str:
        return self.stories[story_id] if 0 <= story_id < len(self.stories) else "Story not found."

    def search_stories(self, query: str) -> list:
        return [story for story in self.stories if query.lower() in story.lower()]

class BookmarkManager:
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager

    def add_bookmark(self, user_id: str, story_id: int) -> None:
        for user in self.user_manager.users:
            if user['username'] == user_id and story_id not in user['bookmarks']:
                user['bookmarks'].append(story_id)
                self.user_manager.save_users()
                break

    def remove_bookmark(self, user_id: str, story_id: int) -> None:
        for user in self.user_manager.users:
            if user['username'] == user_id and story_id in user['bookmarks']:
                user['bookmarks'].remove(story_id)
                self.user_manager.save_users()
                break

    def get_bookmarks(self, user_id: str) -> list:
        for user in self.user_manager.users:
            if user['username'] == user_id:
                return user['bookmarks']
        return []

class User(UserMixin):
    def __init__(self, username):
        self.id = username

user_manager = UserManager()
story_manager = StoryManager()
bookmark_manager = BookmarkManager(user_manager)

@login_manager.user_loader
def load_user(user_id):
    if any(user['username'] == user_id for user in user_manager.users):
        return User(user_id)
    return None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            login_user(User(username))
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your username and password.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username already exists.', 'error')
    return render_template('registration.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', stories=story_manager.stories)

@app.route('/story/<int:story_id>', methods=['GET', 'POST'])
@login_required
def story_details(story_id):
    details = story_manager.get_story_details(story_id)
    if request.method == 'POST':
        user_id = session['user_id']
        bookmark_manager.add_bookmark(user_id, story_id)
        flash('Story added to bookmarks!', 'success')
    return render_template('story_details.html', details=details)

@app.route('/bookmarks')
@login_required
def bookmarks():
    user_id = session['user_id']
    bookmarks = bookmark_manager.get_bookmarks(user_id)
    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8310, debug=False)
