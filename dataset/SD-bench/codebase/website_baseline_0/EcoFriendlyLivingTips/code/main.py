from flask import Flask, render_template, request, redirect, url_for, session
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
            title, content = line.strip().split('|')
            tips.append(Tip(title, content))
    return tips

def load_resources():
    resources = []
    with open('resources.txt', 'r') as file:
        for line in file:
            title, url = line.strip().split('|')
            resources.append(Resource(title, url))
    return resources

def load_forum_posts():
    forum_posts = []
    with open('forum.txt', 'r') as file:
        for line in file:
            username, content = line.strip().split('|')
            forum_posts.append(ForumPost(username, content))
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
                return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    tips = load_tips()
    resources = load_resources()
    return render_template('dashboard.html', tips=tips, resources=resources)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        username = session.get('username')
        content = request.form['content']
        forum_post = ForumPost(username, content)
        forum_post.save()
    forum_posts = load_forum_posts()
    return render_template('forum.html', forum_posts=forum_posts)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        message = request.form['message']
        # Handle contact support logic here
        return render_template('contact.html', success=True)  # Feedback for successful submission
    return render_template('contact.html')

@app.route('/add_resource', methods=['GET', 'POST'])
def add_resource():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        resource = Resource(title, url)
        resource.save()
        return redirect(url_for('dashboard'))
    return render_template('add_resource.html')

@app.route('/add_tip', methods=['GET', 'POST'])
def add_tip():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tip = Tip(title, content)
        tip.save()
        return redirect(url_for('dashboard'))
    return render_template('add_tip.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = session.get('username')
    user = User.load(username)
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        user.username = new_username
        user.password = new_password
        user.save()
        session['username'] = new_username
        return redirect(url_for('dashboard'))
    return render_template('profile.html', user=user)

@app.route('/introduction')
def introduction():
    return render_template('introduction.html')

if __name__ == '__main__':
    app.run(port=8533, debug=False)
