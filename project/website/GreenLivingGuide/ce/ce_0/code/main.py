from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def save_users(self):
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

    def authenticate(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def add_user(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

class TipManager:
    def __init__(self):
        self.tips = []
        self.load_tips()

    def load_tips(self):
        if os.path.exists('tips.txt'):
            with open('tips.txt', 'r') as file:
                self.tips = [line.strip() for line in file]

    def save_tips(self):
        with open('tips.txt', 'w') as file:
            for tip in self.tips:
                file.write(f"{tip}\n")

    def add_tip(self, tip: str) -> bool:
        self.tips.append(tip)
        self.save_tips()
        return True

class ArticleManager:
    def __init__(self):
        self.articles = []
        self.load_articles()

    def load_articles(self):
        if os.path.exists('articles.txt'):
            with open('articles.txt', 'r') as file:
                self.articles = [line.strip() for line in file]

    def save_articles(self):
        with open('articles.txt', 'w') as file:
            for article in self.articles:
                file.write(f"{article}\n")

    def add_article(self, article: str) -> bool:
        self.articles.append(article)
        self.save_articles()
        return True

class ForumManager:
    def __init__(self):
        self.posts = []
        self.load_posts()

    def load_posts(self):
        if os.path.exists('forum.txt'):
            with open('forum.txt', 'r') as file:
                self.posts = [line.strip() for line in file]

    def save_posts(self):
        with open('forum.txt', 'w') as file:
            for post in self.posts:
                file.write(f"{post}\n")

    def add_post(self, post: str) -> bool:
        self.posts.append(post)
        self.save_posts()
        return True

user_manager = UserManager()
tip_manager = TipManager()
article_manager = ArticleManager()
forum_manager = ForumManager()

@login_manager.user_loader
def load_user(username):
    return User(username)

class User(UserMixin):
    def __init__(self, username):
        self.username = username

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.authenticate(username, password):
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', tips=tip_manager.tips, articles=article_manager.articles)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.add_user(username, password):
            return redirect(url_for('login'))
    return render_template('create_account.html')

@app.route('/submit_tip', methods=['POST'])
@login_required
def submit_tip():
    tip = request.form['tip']
    tip_manager.add_tip(tip)
    return redirect(url_for('dashboard'))

@app.route('/submit_article', methods=['POST'])
@login_required
def submit_article():
    article = request.form['article']
    article_manager.add_article(article)
    return redirect(url_for('dashboard'))

@app.route('/post_to_forum', methods=['POST'])
@login_required
def post_to_forum():
    post = request.form['post']
    forum_manager.add_post(post)
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8171, debug=False)
