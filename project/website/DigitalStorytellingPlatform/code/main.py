from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = (password, email)
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username][0] == password:
            return True
        return False

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    self.users[username] = (password, email)

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for username, (password, email) in self.users.items():
                file.write(f"{username}|{password}|{email}\n")

class StoryManager:
    def __init__(self):
        self.stories = {}
        self.load_stories()

    def create_story(self, title: str, content: str) -> None:
        self.stories[title] = content
        self.save_stories()

    def edit_story(self, title: str, content: str) -> None:
        if title in self.stories:
            self.stories[title] = content
            self.save_stories()

    def load_stories(self) -> None:
        if os.path.exists('stories.txt'):
            with open('stories.txt', 'r') as file:
                for line in file:
                    title, content = line.strip().split('|', 1)
                    self.stories[title] = content

    def save_stories(self) -> None:
        with open('stories.txt', 'w') as file:
            for title, content in self.stories.items():
                file.write(f"{title}|{content}\n")

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.story_manager = StoryManager()

    def run(self) -> None:
        app.run(port=8297, debug=False)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app.user_manager.login(username, password):
            return redirect(url_for('story_creation'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if app.user_manager.register(username, password, email):
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose another one.')
    return render_template('register.html')

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        app.story_manager.create_story(title, content)
        return redirect(url_for('story_creation'))
    return render_template('story_creation.html', stories=app.story_manager.stories)

@app.route('/edit_story/<title>', methods=['GET', 'POST'])
def edit_story(title):
    if request.method == 'POST':
        content = request.form['content']
        app.story_manager.edit_story(title, content)
        return redirect(url_for('story_creation'))
    story_content = app.story_manager.stories.get(title, "")
    return render_template('edit_story.html', title=title, content=story_content)

if __name__ == '__main__':
    main = Main()
    main.run()