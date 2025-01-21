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
    with open('forum_posts.txt', 'r') as file:
        for line in file:
            forum_posts.append(ForumPost(line.strip()))
    return forum_posts

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        content = request.form['content']
        tip = Tip(content)
        tip.save()
        return redirect('/tips')
    all_tips = load_tips()
    return render_template('tips.html', tips=all_tips)

@app.route('/resources')
def resources():
    all_resources = load_resources()
    return render_template('resources.html', resources=all_resources)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        content = request.form['content']
        post = ForumPost(content)
        post.save()
        return redirect('/forum')
    all_posts = load_forum_posts()
    return render_template('forum.html', posts=all_posts)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=9031, debug=False)
