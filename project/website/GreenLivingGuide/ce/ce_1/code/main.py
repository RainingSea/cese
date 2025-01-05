from flask import Flask, render_template, request, redirect, url_for, session
from typing import List
import os

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    def validate_password(self, password: str) -> bool:
        return self.password == password


class Tip:
    def __init__(self, content: str, author: str):
        self.content = content
        self.author = author

    def save(self):
        with open('tips.txt', 'a') as f:
            f.write(f"{self.content}|{self.author}\n")


class Article:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self):
        with open('articles.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.author}\n")


class ForumPost:
    def __init__(self, content: str, author: str):
        self.content = content
        self.author = author

    def save(self):
        with open('forum.txt', 'a') as f:
            f.write(f"{self.content}|{self.author}\n")


class App:
    def __init__(self):
        self.users: List[User] = []
        self.tips: List[Tip] = []
        self.articles: List[Article] = []
        self.forum_posts: List[ForumPost] = []
        self.load_data()

    def load_data(self):
        if os.path.exists('users.txt'):
            with open('users.txt') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    self.users.append(User(username, password))

        if os.path.exists('tips.txt'):
            with open('tips.txt') as f:
                for line in f:
                    content, author = line.strip().split('|')
                    self.tips.append(Tip(content, author))

        if os.path.exists('articles.txt'):
            with open('articles.txt') as f:
                for line in f:
                    title, content, author = line.strip().split('|')
                    self.articles.append(Article(title, content, author))

        if os.path.exists('forum.txt'):
            with open('forum.txt') as f:
                for line in f:
                    content, author = line.strip().split('|')
                    self.forum_posts.append(ForumPost(content, author))

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.validate_password(password):
                session['username'] = username
                return True
        return False

    def register(self, username: str, password: str):
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)

    def submit_tip(self, content: str, author: str):
        new_tip = Tip(content, author)
        new_tip.save()
        self.tips.append(new_tip)

    def submit_article(self, title: str, content: str, author: str):
        new_article = Article(title, content, author)
        new_article.save()
        self.articles.append(new_article)

    def submit_forum_post(self, content: str, author: str):
        new_post = ForumPost(content, author)
        new_post.save()
        self.forum_posts.append(new_post)


app = Flask(__name__)
app.secret_key = 'your_secret_key'
application = App()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', tips=application.tips, articles=application.articles)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if application.login(username, password):
        return redirect(url_for('dashboard'))
    return "Login failed", 401

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    application.register(username, password)
    return redirect(url_for('login'))

@app.route('/submit_tip', methods=['POST'])
def submit_tip():
    content = request.form['content']
    author = session.get('username', 'Anonymous')
    application.submit_tip(content, author)
    return redirect(url_for('dashboard'))

@app.route('/submit_article', methods=['POST'])
def submit_article():
    title = request.form['title']
    content = request.form['content']
    author = session.get('username', 'Anonymous')
    application.submit_article(title, content, author)
    return redirect(url_for('dashboard'))

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        content = request.form['content']
        author = session.get('username', 'Anonymous')
        application.submit_forum_post(content, author)
    return render_template('forum.html', posts=application.forum_posts)


if __name__ == '__main__':
    app.run(port=8027, debug=False)
