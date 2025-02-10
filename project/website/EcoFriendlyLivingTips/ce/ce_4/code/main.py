from flask import Flask, render_template, request, redirect, url_for, session
from typing import List
import os

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.profile_info = {}

    def update_profile(self, info: dict):
        self.profile_info.update(info)

class Tip:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

class Resource:
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url

class ForumPost:
    def __init__(self, username: str, content: str):
        self.username = username
        self.content = content

class EcoFriendlyLivingTipsApp:
    def __init__(self):
        self.users = []
        self.tips = []
        self.resources = []
        self.forum_posts = []
        self.load_data()

    def load_data(self):
        self.load_users()
        self.load_tips()
        self.load_resources()
        self.load_forum_posts()

    def save_data(self):
        self.save_users()
        self.save_tips()
        self.save_resources()
        self.save_forum_posts()

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

    def load_users(self):
        if os.path.exists("users.txt"):
            with open("users.txt", "r") as f:
                for line in f:
                    username, password = line.strip().split("|")
                    self.users.append(User(username, password))

    def save_users(self):
        with open("users.txt", "w") as f:
            for user in self.users:
                f.write(f"{user.username}|{user.password}\n")

    def load_tips(self):
        if os.path.exists("tips.txt"):
            with open("tips.txt", "r") as f:
                for line in f:
                    title, content = line.strip().split("|")
                    self.tips.append(Tip(title, content))

    def save_tips(self):
        with open("tips.txt", "w") as f:
            for tip in self.tips:
                f.write(f"{tip.title}|{tip.content}\n")

    def load_resources(self):
        if os.path.exists("resources.txt"):
            with open("resources.txt", "r") as f:
                for line in f:
                    title, url = line.strip().split("|")
                    self.resources.append(Resource(title, url))

    def save_resources(self):
        with open("resources.txt", "w") as f:
            for resource in self.resources:
                f.write(f"{resource.title}|{resource.url}\n")

    def load_forum_posts(self):
        if os.path.exists("forum.txt"):
            with open("forum.txt", "r") as f:
                for line in f:
                    username, content = line.strip().split("|")
                    self.forum_posts.append(ForumPost(username, content))

    def save_forum_posts(self):
        with open("forum.txt", "w") as f:
            for post in self.forum_posts:
                f.write(f"{post.username}|{post.content}\n")

app = Flask(__name__)
app.secret_key = 'your_secret_key'
eco_app = EcoFriendlyLivingTipsApp()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in eco_app.users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'], tips=eco_app.tips, resources=eco_app.resources, forum_posts=eco_app.forum_posts)
    return redirect(url_for('login'))

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        eco_app.add_tip(Tip(title, content))
        return redirect(url_for('tips'))
    return render_template('tips.html', tips=eco_app.tips)

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        eco_app.add_resource(Resource(title, url))
        return redirect(url_for('resources'))
    return render_template('resources.html', resources=eco_app.resources)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        content = request.form['content']
        eco_app.add_forum_post(ForumPost(session['username'], content))
        return redirect(url_for('forum'))
    return render_template('forum.html', forum_posts=eco_app.forum_posts)

@app.route('/profile')
def profile():
    return render_template('profile.html', username=session['username'])

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=8627, debug=False)
