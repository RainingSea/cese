from flask import Flask, render_template, request, redirect, url_for, session
from typing import List
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def to_string(self) -> str:
        return f"{self.username}|{self.password}|{self.email}"

class Tip:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def to_string(self) -> str:
        return f"{self.title}|{self.content}"

class Resource:
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url

    def to_string(self) -> str:
        return f"{self.title}|{self.url}"

class ForumPost:
    def __init__(self, username: str, content: str):
        self.username = username
        self.content = content

    def to_string(self) -> str:
        return f"{self.username}|{self.content}"

class EcoFriendlyLivingTipsApp:
    def __init__(self):
        self.users: List[User] = []
        self.tips: List[Tip] = []
        self.resources: List[Resource] = []
        self.forum_posts: List[ForumPost] = []
        self.load_data()

    def load_data(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    self.users.append(User(username, password, email))

        if os.path.exists('tips.txt'):
            with open('tips.txt', 'r') as f:
                for line in f:
                    title, content = line.strip().split('|')
                    self.tips.append(Tip(title, content))

        if os.path.exists('resources.txt'):
            with open('resources.txt', 'r') as f:
                for line in f:
                    title, url = line.strip().split('|')
                    self.resources.append(Resource(title, url))

        if os.path.exists('forum.txt'):
            with open('forum.txt', 'r') as f:
                for line in f:
                    username, content = line.strip().split('|')
                    self.forum_posts.append(ForumPost(username, content))

    def save_data(self):
        with open('users.txt', 'w') as f:
            for user in self.users:
                f.write(user.to_string() + '\n')

        with open('tips.txt', 'w') as f:
            for tip in self.tips:
                f.write(tip.to_string() + '\n')

        with open('resources.txt', 'w') as f:
            for resource in self.resources:
                f.write(resource.to_string() + '\n')

        with open('forum.txt', 'w') as f:
            for post in self.forum_posts:
                f.write(post.to_string() + '\n')

    def add_user(self, user: User):
        self.users.append(user)
        self.save_data()

    def add_tip(self, tip: Tip):
        self.tips.append(tip)
        self.save_data()

    def add_resource(self, resource: Resource):
        self.resources.append(resource)
        self.save_data()

    def add_forum_post(self, post: ForumPost):
        self.forum_posts.append(post)
        self.save_data()

    def get_tips(self) -> List[Tip]:
        return self.tips

    def get_resources(self) -> List[Resource]:
        return self.resources

    def get_forum_posts(self) -> List[ForumPost]:
        return self.forum_posts

eco_app = EcoFriendlyLivingTipsApp()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        eco_app.add_user(User(username, password, email))
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    tips = eco_app.get_tips()
    resources = eco_app.get_resources()
    return render_template('dashboard.html', tips=tips, resources=resources)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        username = request.form['username']
        content = request.form['content']
        eco_app.add_forum_post(ForumPost(username, content))
        return redirect(url_for('forum'))
    posts = eco_app.get_forum_posts()
    return render_template('forum.html', posts=posts)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=9028, debug=False)
