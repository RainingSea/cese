from flask import Flask, render_template, request, redirect, session
from user import User
from tip import Tip
from resource import Resource
from forum_post import ForumPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_tips():
    tips = []
    with open('tips.txt', 'r') as file:
        for line in file:
            tips.append(Tip(line.strip()))
    return tips

def load_resources():
    resources = []
    with open('resources.txt', 'r') as file:
        for line in file:
            resources.append(Resource(line.strip()))
    return resources

def load_forum_posts():
    forum_posts = []
    with open('forum.txt', 'r') as file:
        for line in file:
            forum_posts.append(ForumPost(line.strip()))
    return forum_posts

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    tips = load_tips()
    resources = load_resources()
    return render_template('dashboard.html', tips=tips, resources=resources)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        content = request.form['content']
        post = ForumPost(content)
        post.save()
    forum_posts = load_forum_posts()
    return render_template('forum.html', forum_posts=forum_posts)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        message = request.form['message']
        # Handle contact support logic here
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=9032, debug=False)
