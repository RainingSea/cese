from flask import Flask, render_template, request, redirect, url_for, session
from typing import List
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Data file paths
USERS_FILE = 'users.txt'
TIPS_FILE = 'tips.txt'
ARTICLES_FILE = 'articles.txt'
FORUM_FILE = 'forum.txt'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def to_string(self) -> str:
        return f"{self.username}|{self.password}"

class Tip:
    def __init__(self, tip: str):
        self.tip = tip

    def to_string(self) -> str:
        return self.tip

class Article:
    def __init__(self, article: str):
        self.article = article

    def to_string(self) -> str:
        return self.article

class ForumPost:
    def __init__(self, post: str):
        self.post = post

    def to_string(self) -> str:
        return self.post

def load_users() -> List[User]:
    users = []
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    return users

def save_user(user: User):
    with open(USERS_FILE, 'a') as file:
        file.write(user.to_string() + '\n')

def load_tips() -> List[Tip]:
    tips = []
    if os.path.exists(TIPS_FILE):
        with open(TIPS_FILE, 'r') as file:
            for line in file:
                tips.append(Tip(line.strip()))
    return tips

def load_articles() -> List[Article]:
    articles = []
    if os.path.exists(ARTICLES_FILE):
        with open(ARTICLES_FILE, 'r') as file:
            for line in file:
                articles.append(Article(line.strip()))
    return articles

def load_forum_posts() -> List[ForumPost]:
    posts = []
    if os.path.exists(FORUM_FILE):
        with open(FORUM_FILE, 'r') as file:
            for line in file:
                posts.append(ForumPost(line.strip()))
    return posts

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        save_user(user)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    tips = load_tips()
    articles = load_articles()
    return render_template('dashboard.html', tips=tips, articles=articles)

@app.route('/submit_tip', methods=['POST'])
def submit_tip():
    tip_content = request.form['tip']
    tip = Tip(tip_content)
    with open(TIPS_FILE, 'a') as file:
        file.write(tip.to_string() + '\n')
    return redirect(url_for('dashboard'))

@app.route('/submit_article', methods=['POST'])
def submit_article():
    article_content = request.form['article']
    article = Article(article_content)
    with open(ARTICLES_FILE, 'a') as file:
        file.write(article.to_string() + '\n')
    return redirect(url_for('dashboard'))

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        post_content = request.form['post']
        post = ForumPost(post_content)
        with open(FORUM_FILE, 'a') as file:
            file.write(post.to_string() + '\n')
        return redirect(url_for('forum'))
    posts = load_forum_posts()
    return render_template('forum.html', posts=posts)

if __name__ == '__main__':
    app.run(port=8542, debug=False)
