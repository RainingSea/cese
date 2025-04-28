from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

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
        return self.users.get(username) == password

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

    def get_story_details(self, story_id: int) -> str:
        return self.stories[story_id] if 0 <= story_id < len(self.stories) else "Story not found."

    def search_stories(self, query: str) -> list:
        return [story for story in self.stories if query.lower() in story.lower()]

    def bookmark_story(self, username: str, story_id: int) -> None:
        # Placeholder for bookmarking logic
        pass

    def get_bookmarked_stories(self, username: str) -> list:
        # Placeholder for retrieving bookmarked stories
        return []

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
        else:
            return "Registration failed. Username already exists."
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', stories=story_manager.stories)

@app.route('/story/<int:story_id>')
def story_details(story_id):
    details = story_manager.get_story_details(story_id)
    return render_template('story_details.html', details=details)

@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html')

if __name__ == '__main__':
    app.run(port=8307, debug=False)
