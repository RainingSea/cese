from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load_users():
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

class Tip:
    def __init__(self, content: str):
        self.content = content

    def save(self):
        with open('tips.txt', 'a') as f:
            f.write(f"{self.content}\n")

    @staticmethod
    def load_tips():
        tips = []
        if os.path.exists('tips.txt'):
            with open('tips.txt', 'r') as f:
                for line in f:
                    tips.append(line.strip())
        return tips

class Article:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self):
        with open('articles.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}\n")

    @staticmethod
    def load_articles():
        articles = []
        if os.path.exists('articles.txt'):
            with open('articles.txt', 'r') as f:
                for line in f:
                    title, content = line.strip().split('|')
                    articles.append(Article(title, content))
        return articles

class ForumPost:
    def __init__(self, username: str, content: str):
        self.username = username
        self.content = content

    def save(self):
        with open('forum.txt', 'a') as f:
            f.write(f"{self.username}|{self.content}\n")

    @staticmethod
    def load_posts():
        posts = []
        if os.path.exists('forum.txt'):
            with open('forum.txt', 'r') as f:
                for line in f:
                    username, content = line.strip().split('|')
                    posts.append(ForumPost(username, content))
        return posts

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_users = User.load_users()
        if username in [user.username for user in existing_users]:
            return "Username already exists. Please choose another."
        else:
            user = User(username, password)
            user.save()
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    articles = Article.load_articles()
    tips = Tip.load_tips()
    return render_template('dashboard.html', articles=articles, tips=tips)

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        tip_content = request.form['tip']
        tip = Tip(tip_content)
        tip.save()
        return redirect(url_for('tips'))
    return render_template('tips.html')

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        article = Article(title, content)
        article.save()
        return redirect(url_for('articles'))
    return render_template('articles.html')

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        post_content = request.form['post']
        username = session.get('username', 'Guest')
        forum_post = ForumPost(username, post_content)
        forum_post.save()
        return redirect(url_for('forum'))
    posts = ForumPost.load_posts()
    return render_template('forum.html', posts=posts)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8132, debug=True)
