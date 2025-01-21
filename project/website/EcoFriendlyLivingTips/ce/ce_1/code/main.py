from flask import Flask, render_template, request, redirect, url_for, session
from typing import List
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Data structures
class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def to_string(self) -> str:
        return f"{self.username}|{self.password}"

class Tip:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def to_string(self) -> str:
        return f"{self.title}|{self.content}"

class Resource:
    def __init__(self, title: str, link: str):
        self.title = title
        self.link = link

    def to_string(self) -> str:
        return f"{self.title}|{self.link}"

class ForumPost:
    def __init__(self, username: str, content: str):
        self.username = username
        self.content = content

    def to_string(self) -> str:
        return f"{self.username}|{self.content}"

class EcoFriendlyLivingTips:
    def __init__(self):
        self.users = self.load_users()
        self.tips = self.load_tips()
        self.resources = self.load_resources()
        self.forum_posts = self.load_forum_posts()

    def load_users(self) -> List[User]:
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def load_tips(self) -> List[Tip]:
        tips = []
        if os.path.exists('tips.txt'):
            with open('tips.txt', 'r') as file:
                for line in file:
                    title, content = line.strip().split('|')
                    tips.append(Tip(title, content))
        return tips

    def load_resources(self) -> List[Resource]:
        resources = []
        if os.path.exists('resources.txt'):
            with open('resources.txt', 'r') as file:
                for line in file:
                    title, link = line.strip().split('|')
                    resources.append(Resource(title, link))
        return resources

    def load_forum_posts(self) -> List[ForumPost]:
        forum_posts = []
        if os.path.exists('forum.txt'):
            with open('forum.txt', 'r') as file:
                for line in file:
                    username, content = line.strip().split('|')
                    forum_posts.append(ForumPost(username, content))
        return forum_posts

    def register_user(self, username: str, password: str) -> None:
        self.users.append(User(username, password))
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")

    def login_user(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def submit_tip(self, title: str, content: str) -> None:
        self.tips.append(Tip(title, content))
        with open('tips.txt', 'a') as file:
            file.write(f"{title}|{content}\n")

    def add_resource(self, title: str, link: str) -> None:
        self.resources.append(Resource(title, link))
        with open('resources.txt', 'a') as file:
            file.write(f"{title}|{link}\n")

    def post_to_forum(self, username: str, content: str) -> None:
        self.forum_posts.append(ForumPost(username, content))
        with open('forum.txt', 'a') as file:
            file.write(f"{username}|{content}\n")

    def get_tips(self) -> List[Tip]:
        return self.tips

    def get_resources(self) -> List[Resource]:
        return self.resources

    def get_forum_posts(self) -> List[ForumPost]:
        return self.forum_posts

eco_friendly_app = EcoFriendlyLivingTips()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        eco_friendly_app.register_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    tips = eco_friendly_app.get_tips()
    return render_template('dashboard.html', tips=tips)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if eco_friendly_app.login_user(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        eco_friendly_app.submit_tip(title, content)
        return redirect(url_for('tips'))
    tips = eco_friendly_app.get_tips()
    return render_template('tips.html', tips=tips)

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if request.method == 'POST':
        title = request.form['title']
        link = request.form['link']
        eco_friendly_app.add_resource(title, link)
        return redirect(url_for('resources'))
    resources = eco_friendly_app.get_resources()
    return render_template('resources.html', resources=resources)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        username = session.get('username')
        content = request.form['content']
        eco_friendly_app.post_to_forum(username, content)
        return redirect(url_for('forum'))
    posts = eco_friendly_app.get_forum_posts()
    return render_template('forum.html', posts=posts)

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=9029, debug=False)
