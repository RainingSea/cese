from flask import Flask, render_template, request, redirect, session, url_for
from user import User
from tip import Tip
from resource import Resource
from forum_post import ForumPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'
eco_friendly_tips = []

class EcoFriendlyLivingTips:
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

    def load_users(self):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                user = User(username, password)
                self.users.append(user)

    def load_tips(self):
        with open('tips.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                tip = Tip(title, content)
                self.tips.append(tip)

    def load_resources(self):
        with open('resources.txt', 'r') as file:
            for line in file:
                title, url = line.strip().split('|')
                resource = Resource(title, url)
                self.resources.append(resource)

    def load_forum_posts(self):
        with open('forum.txt', 'r') as file:
            for line in file:
                username, content = line.strip().split('|')
                post = ForumPost(username, content)
                self.forum_posts.append(post)

    def register(self, username: str, password: str):
        user = User(username, password)
        self.users.append(user)
        user.save()

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                session['username'] = username
                return True
        return False

    def submit_tip(self, title: str, content: str):
        tip = Tip(title, content)
        self.tips.append(tip)
        tip.save()

    def submit_resource(self, title: str, url: str):
        resource = Resource(title, url)
        self.resources.append(resource)
        resource.save()

    def submit_forum_post(self, username: str, content: str):
        post = ForumPost(username, content)
        self.forum_posts.append(post)
        post.save()

eco_friendly_living_tips = EcoFriendlyLivingTips()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', tips=eco_friendly_living_tips.tips, resources=eco_friendly_living_tips.resources)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if eco_friendly_living_tips.login(username, password):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/submit_tip', methods=['POST'])
def submit_tip():
    title = request.form['title']
    content = request.form['content']
    eco_friendly_living_tips.submit_tip(title, content)
    return redirect(url_for('dashboard'))

@app.route('/submit_resource', methods=['POST'])
def submit_resource():
    title = request.form['title']
    url = request.form['url']
    eco_friendly_living_tips.submit_resource(title, url)
    return redirect(url_for('dashboard'))

@app.route('/submit_forum_post', methods=['POST'])
def submit_forum_post():
    content = request.form['content']
    username = session.get('username', 'Anonymous')
    eco_friendly_living_tips.submit_forum_post(username, content)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=8625, debug=False)
