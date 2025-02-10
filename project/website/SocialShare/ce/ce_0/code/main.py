from flask import Flask, render_template, request, redirect, url_for, session
from typing import List
import os

class User:
    def __init__(self, username: str, password: str, bio: str):
        self.username = username
        self.password = password
        self.bio = bio

    def update_bio(self, new_bio: str):
        self.bio = new_bio

class Article:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

class Comment:
    def __init__(self, article_id: int, user: str, comment_text: str):
        self.article_id = article_id
        self.user = user
        self.comment_text = comment_text

class SocialShareApp:
    def __init__(self):
        self.users = self.load_users()
        self.articles = self.load_articles()
        self.comments = self.load_comments()

    def load_users(self) -> List[User]:
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, bio = line.strip().split('|')
                    users.append(User(username, password, bio))
        return users

    def load_articles(self) -> List[Article]:
        articles = []
        if os.path.exists('articles.txt'):
            with open('articles.txt', 'r') as f:
                for line in f:
                    title, content, author = line.strip().split('|')
                    articles.append(Article(title, content, author))
        return articles

    def load_comments(self) -> List[Comment]:
        comments = []
        if os.path.exists('comments.txt'):
            with open('comments.txt', 'r') as f:
                for line in f:
                    article_id, user, comment_text = line.strip().split('|')
                    comments.append(Comment(int(article_id), user, comment_text))
        return comments

    def register(self, username: str, password: str, bio: str):
        new_user = User(username, password, bio)
        self.users.append(new_user)
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}|{bio}\n")

    def login(self, username: str, password: str) -> User:
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None

    def share_article(self, title: str, content: str, author: str):
        new_article = Article(title, content, author)
        self.articles.append(new_article)
        with open('articles.txt', 'a') as f:
            f.write(f"{title}|{content}|{author}\n")

    def add_comment(self, article_id: int, user: str, comment_text: str):
        new_comment = Comment(article_id, user, comment_text)
        self.comments.append(new_comment)
        with open('comments.txt', 'a') as f:
            f.write(f"{article_id}|{user}|{comment_text}\n")

    def get_feed(self) -> List[Article]:
        return self.articles

app = Flask(__name__)
app.secret_key = 'your_secret_key'
social_share_app = SocialShareApp()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        bio = request.form['bio']
        social_share_app.register(username, password, bio)
        return redirect(url_for('login_page'))
    return render_template('registration.html')

@app.route('/feed')
def feed():
    articles = social_share_app.get_feed()
    return render_template('feed.html', articles=articles)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = social_share_app.login(username, password)
    if user:
        session['username'] = user.username
        return redirect(url_for('feed'))
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(port=8641, debug=False)
