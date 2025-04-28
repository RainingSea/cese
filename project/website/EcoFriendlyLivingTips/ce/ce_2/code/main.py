import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users[username] = password
        return True

    def update_profile(self, username: str, new_data: dict) -> bool:
        # Simplified for this example; would require more logic in a real app
        return True

class TipManager:
    def __init__(self, tips_file: str):
        self.tips_file = tips_file
        self.load_tips()

    def load_tips(self):
        self.tips = []
        if os.path.exists(self.tips_file):
            with open(self.tips_file, 'r') as file:
                self.tips = [line.strip() for line in file]

    def get_tips(self) -> list:
        return self.tips

    def submit_tip(self, tip: str) -> bool:
        with open(self.tips_file, 'a') as file:
            file.write(f"{tip}\n")
        self.tips.append(tip)
        return True

class ResourceManager:
    def __init__(self, resources_file: str):
        self.resources_file = resources_file
        self.load_resources()

    def load_resources(self):
        self.resources = []
        if os.path.exists(self.resources_file):
            with open(self.resources_file, 'r') as file:
                self.resources = [line.strip() for line in file]

    def get_resources(self) -> list:
        return self.resources

    def add_resource(self, resource: str) -> bool:
        with open(self.resources_file, 'a') as file:
            file.write(f"{resource}\n")
        self.resources.append(resource)
        return True

class ForumManager:
    def __init__(self, forum_file: str):
        self.forum_file = forum_file
        self.load_posts()

    def load_posts(self):
        self.posts = []
        if os.path.exists(self.forum_file):
            with open(self.forum_file, 'r') as file:
                self.posts = [line.strip() for line in file]

    def get_posts(self) -> list:
        return self.posts

    def submit_post(self, post: str) -> bool:
        with open(self.forum_file, 'a') as file:
            file.write(f"{post}\n")
        self.posts.append(post)
        return True

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login_page'))
    return render_template('register.html')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/tips')
def tips_page():
    tips = tip_manager.get_tips()
    return render_template('tips.html', tips=tips)

@app.route('/resources')
def resources_page():
    resources = resource_manager.get_resources()
    return render_template('resources.html', resources=resources)

@app.route('/forum')
def forum_page():
    posts = forum_manager.get_posts()
    return render_template('forum.html', posts=posts)

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

if __name__ == '__main__':
    user_manager = UserManager('users.txt')
    tip_manager = TipManager('tips.txt')
    resource_manager = ResourceManager('resources.txt')
    forum_manager = ForumManager('forum_posts.txt')
    app.run(port=8329, debug=False)
