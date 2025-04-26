from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
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
        if any(user[0] == username for user in self.users):
            return False
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

    def load_stories(self):
        if not os.path.exists('stories.txt'):
            return []
        with open('stories.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def get_all_stories(self):
        return self.stories

    def get_story_details(self, title: str):
        for story in self.stories:
            if story[0] == title:
                return story
        return None

    def search_stories(self, query: str):
        return [story for story in self.stories if query.lower() in story[0].lower()]

class BookmarkManager:
    def __init__(self):
        self.bookmarks = self.load_bookmarks()

    def load_bookmarks(self):
        if not os.path.exists('bookmarks.txt'):
            return {}
        bookmarks = {}
        with open('bookmarks.txt', 'r') as file:
            for line in file:
                username, title = line.strip().split('|')
                if username in bookmarks:
                    bookmarks[username].append(title)
                else:
                    bookmarks[username] = [title]
        return bookmarks

    def add_bookmark(self, username: str, story_title: str) -> bool:
        if username not in self.bookmarks:
            self.bookmarks[username] = []
        if story_title in self.bookmarks[username]:
            return False
        self.bookmarks[username].append(story_title)
        with open('bookmarks.txt', 'a') as file:
            file.write(f"{username}|{story_title}\n")
        return True

    def get_bookmarks(self, username: str):
        return self.bookmarks.get(username, [])

    def remove_bookmark(self, username: str, story_title: str) -> bool:
        if username in self.bookmarks and story_title in self.bookmarks[username]:
            self.bookmarks[username].remove(story_title)
            self.save_bookmarks()
            return True
        return False

    def save_bookmarks(self):
        with open('bookmarks.txt', 'w') as file:
            for username, titles in self.bookmarks.items():
                for title in titles:
                    file.write(f"{username}|{title}\n")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', stories=story_manager.get_all_stories())

@app.route('/story/<title>')
def story_details(title):
    story = story_manager.get_story_details(title)
    return render_template('story_details.html', story=story)

@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html', bookmarks=bookmark_manager.get_bookmarks(session.get('username')))

user_manager = UserManager()
story_manager = StoryManager()
bookmark_manager = BookmarkManager()

if __name__ == '__main__':
    app.run(port=8145, debug=False)
