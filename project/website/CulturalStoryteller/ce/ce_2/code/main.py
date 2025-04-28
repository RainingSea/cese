from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username:
                return False  # User already exists
        self.users.append([username, password])
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

class StoryManager:
    def __init__(self):
        self.stories = self.load_stories()
        self.bookmarks = self.load_bookmarks()

    def load_stories(self):
        if not os.path.exists('stories.txt'):
            return []
        with open('stories.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def load_bookmarks(self):
        if not os.path.exists('bookmarks.txt'):
            return {}
        bookmarks = {}
        with open('bookmarks.txt', 'r') as file:
            for line in file.readlines():
                username, story_id = line.strip().split('|')
                if username not in bookmarks:
                    bookmarks[username] = []
                bookmarks[username].append(int(story_id))
        return bookmarks

    def get_all_stories(self):
        return self.stories

    def get_story_details(self, story_id: int):
        return self.stories[story_id]

    def search_stories(self, query: str):
        return [story for story in self.stories if query.lower() in story[0].lower()]

    def add_bookmark(self, username: str, story_id: int) -> bool:
        if username not in self.bookmarks:
            self.bookmarks[username] = []
        if story_id in self.bookmarks[username]:
            return False  # Already bookmarked
        self.bookmarks[username].append(story_id)
        with open('bookmarks.txt', 'a') as file:
            file.write(f"{username}|{story_id}\n")
        return True

    def get_bookmarks(self, username: str):
        return self.bookmarks.get(username, [])

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
        return redirect(url_for('login'))
    return "Registration Failed"

@app.route('/dashboard')
def dashboard():
    stories = story_manager.get_all_stories()
    return render_template('dashboard.html', stories=stories)

@app.route('/story/<int:story_id>')
def story_details(story_id):
    story = story_manager.get_story_details(story_id)
    return render_template('story_details.html', story=story)

@app.route('/bookmarks')
def bookmarks():
    username = session.get('username')
    bookmarks = story_manager.get_bookmarks(username)
    return render_template('bookmarks.html', bookmarks=bookmarks)

if __name__ == '__main__':
    app.run(port=8309, debug=False)
