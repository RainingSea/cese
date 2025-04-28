import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str, email: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append([username, password, email])
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')

    def login(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)

class StoryManager:
    def __init__(self):
        self.stories = self.load_stories()

    def load_stories(self):
        if not os.path.exists('stories.txt'):
            return []
        with open('stories.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def create_story(self, title: str, content: str) -> bool:
        self.stories.append([title, content])
        return self.save_story()

    def edit_story(self, title: str, content: str) -> bool:
        for story in self.stories:
            if story[0] == title:
                story[1] = content
                return self.save_story()
        return False

    def save_story(self) -> bool:
        with open('stories.txt', 'w') as file:
            for story in self.stories:
                file.write('|'.join(story) + '\n')
        return True

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
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        story_manager.create_story(title, content)
        return redirect(url_for('story_creation'))
    return render_template('story_creation.html')

if __name__ == '__main__':
    app.run(port=8323, debug=False)
