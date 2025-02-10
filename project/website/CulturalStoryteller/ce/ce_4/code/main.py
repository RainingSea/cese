from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

class Story:
    def __init__(self, title: str, content: str, cultural_origin: str):
        self.title = title
        self.content = content
        self.cultural_origin = cultural_origin

class Bookmark:
    def __init__(self, username: str, story_title: str):
        self.username = username
        self.story_title = story_title

    def save(self):
        with open('bookmarks.txt', 'a') as f:
            f.write(f"{self.username}|{self.story_title}\n")

class App:
    @staticmethod
    def register(username: str, password: str):
        user = User(username, password)
        user.save()

    @staticmethod
    def login(username: str, password: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

    @staticmethod
    def get_stories() -> list:
        stories = []
        if os.path.exists('stories.txt'):
            with open('stories.txt', 'r') as f:
                for line in f:
                    title, content, cultural_origin = line.strip().split('|')
                    stories.append(Story(title, content, cultural_origin))
        return stories

    @staticmethod
    def get_story_details(title: str) -> Story:
        if os.path.exists('stories.txt'):
            with open('stories.txt', 'r') as f:
                for line in f:
                    story_title, content, cultural_origin = line.strip().split('|')
                    if story_title == title:
                        return Story(story_title, content, cultural_origin)
        return None

    @staticmethod
    def add_bookmark(username: str, story_title: str):
        bookmark = Bookmark(username, story_title)
        bookmark.save()

    @staticmethod
    def get_bookmarks(username: str) -> list:
        bookmarks = []
        if os.path.exists('bookmarks.txt'):
            with open('bookmarks.txt', 'r') as f:
                for line in f:
                    stored_username, story_title = line.strip().split('|')
                    if stored_username == username:
                        bookmarks.append(story_title)
        return bookmarks

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if App.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        App.register(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    stories = App.get_stories()
    return render_template('dashboard.html', stories=stories)

@app.route('/story/<title>')
def story_details(title):
    story = App.get_story_details(title)
    return render_template('story_details.html', story=story)

@app.route('/bookmarks')
def bookmarks():
    username = session.get('username')
    user_bookmarks = App.get_bookmarks(username)
    return render_template('bookmarks.html', bookmarks=user_bookmarks)

if __name__ == '__main__':
    app.run(port=8609, debug=False)
