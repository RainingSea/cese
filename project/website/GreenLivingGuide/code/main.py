from flask import Flask, render_template, redirect, url_for, request, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

# Data file paths
USER_DATA_FILE = 'users.txt'
TIP_DATA_FILE = 'tips.txt'
ARTICLE_DATA_FILE = 'articles.txt'
FORUM_DATA_FILE = 'forum.txt'

class User(UserMixin):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open(USER_DATA_FILE, 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load(username: str):
        with open(USER_DATA_FILE, 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1])
        return None

class Tip:
    def __init__(self, content: str):
        self.content = content

    def save(self):
        with open(TIP_DATA_FILE, 'a') as f:
            f.write(f"{self.content}\n")

class Article:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self):
        with open(ARTICLE_DATA_FILE, 'a') as f:
            f.write(f"{self.title}|{self.content}\n")

class ForumPost:
    def __init__(self, username: str, content: str):
        self.username = username
        self.content = content

    def save(self):
        with open(FORUM_DATA_FILE, 'a') as f:
            f.write(f"{self.username}|{self.content}\n")

@login_manager.user_loader
def load_user(user_id):
    return User.load(user_id)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User.load(username)
    if user and user.password == password:
        login_user(user)
        return redirect(url_for('dashboard'))
    return 'Invalid username or password', 401

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    new_user = User(username, password)
    new_user.save()
    return redirect(url_for('login'))

@app.route('/tips', methods=['GET', 'POST'])
@login_required
def tips():
    if request.method == 'POST':
        tip_content = request.form['tip']
        new_tip = Tip(tip_content)
        new_tip.save()
        return redirect(url_for('tips'))
    with open(TIP_DATA_FILE, 'r') as f:
        tips = f.readlines()
    return render_template('tips.html', tips=tips)

@app.route('/articles', methods=['GET', 'POST'])
@login_required
def articles():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_article = Article(title, content)
        new_article.save()
        return redirect(url_for('articles'))
    with open(ARTICLE_DATA_FILE, 'r') as f:
        articles = f.readlines()
    return render_template('articles.html', articles=articles)

@app.route('/forum', methods=['GET', 'POST'])
@login_required
def forum():
    if request.method == 'POST':
        post_content = request.form['post']
        new_post = ForumPost(current_user.username, post_content)
        new_post.save()
        return redirect(url_for('forum'))
    with open(FORUM_DATA_FILE, 'r') as f:
        posts = f.readlines()
    return render_template('forum.html', posts=posts)

if __name__ == '__main__':
    app.run(port=8173, debug=False)
