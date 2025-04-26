from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username] == password:
            session['username'] = username
            return True
        return False

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

class StoryManager:
    def __init__(self):
        self.stories = []
        self.load_stories()

    def load_stories(self) -> None:
        if os.path.exists('stories.txt'):
            with open('stories.txt', 'r') as file:
                for line in file:
                    self.stories.append(line.strip())

    def get_story(self, story_id: int) -> str:
        return self.stories[story_id] if 0 <= story_id < len(self.stories) else ""

    def search_stories(self, query: str) -> list:
        return [story for story in self.stories if query.lower() in story.lower()]

    def bookmark_story(self, user: str, story_id: int) -> None:
        with open(f"{user}_bookmarks.txt", 'a') as file:
            file.write(f"{story_id}\n")

    def get_bookmarked_stories(self, user: str) -> list:
        bookmarks = []
        if os.path.exists(f"{user}_bookmarks.txt"):
            with open(f"{user}_bookmarks.txt", 'r') as file:
                bookmarks = [int(line.strip()) for line in file]
        return bookmarks

user_manager = UserManager()
story_manager = StoryManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if user_manager.register(username, password):
        return redirect('/')
    return "Registration failed", 400

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', stories=story_manager.stories)

@app.route('/story/<int:story_id>')
def story_details(story_id):
    story = story_manager.get_story(story_id)
    return render_template('story_details.html', story=story)

@app.route('/bookmark/<int:story_id>')
def bookmark(story_id):
    if 'username' in session:
        story_manager.bookmark_story(session['username'], story_id)
    return redirect('/dashboard')

@app.route('/bookmarks')
def bookmarks():
    if 'username' in session:
        bookmarked_stories = story_manager.get_bookmarked_stories(session['username'])
        return render_template('bookmarks.html', stories=bookmarked_stories)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8144, debug=False)
