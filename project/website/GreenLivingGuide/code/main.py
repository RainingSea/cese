from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

class Article:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self):
        with open('articles.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.author}\n")

class Tip:
    def __init__(self, content: str, author: str):
        self.content = content
        self.author = author

    def save(self):
        with open('tips.txt', 'a') as f:
            f.write(f"{self.content}|{self.author}\n")

class ForumPost:
    def __init__(self, content: str, author: str):
        self.content = content
        self.author = author

    def save(self):
        with open('forum.txt', 'a') as f:
            f.write(f"{self.content}|{self.author}\n")

def load_users():
    users = {}
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users[username] = password
    return users

def load_articles():
    articles = []
    if os.path.exists('articles.txt'):
        with open('articles.txt', 'r') as f:
            for line in f:
                title, content, author = line.strip().split('|')
                articles.append(Article(title, content, author))
    return articles

def load_tips():
    tips = []
    if os.path.exists('tips.txt'):
        with open('tips.txt', 'r') as f:
            for line in f:
                content, author = line.strip().split('|')
                tips.append(Tip(content, author))
    return tips

def load_forum_posts():
    forum_posts = []
    if os.path.exists('forum.txt'):
        with open('forum.txt', 'r') as f:
            for line in f:
                content, author = line.strip().split('|')
                forum_posts.append(ForumPost(content, author))
    return forum_posts

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials, please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            return "Username already exists."
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    articles = load_articles()
    tips = load_tips()
    return render_template('dashboard.html', username=session['username'], articles=articles, tips=tips)

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        content = request.form['content']
        new_tip = Tip(content, session['username'])
        new_tip.save()
        return redirect(url_for('tips'))
    tips_list = load_tips()
    return render_template('tips.html', username=session['username'], tips=tips_list)

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_article = Article(title, content, session['username'])
        new_article.save()
        return redirect(url_for('articles'))
    articles_list = load_articles()
    return render_template('articles.html', username=session['username'], articles=articles_list)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        content = request.form['content']
        new_post = ForumPost(content, session['username'])
        new_post.save()
        return redirect(url_for('forum'))
    forum_posts = load_forum_posts()
    return render_template('forum.html', username=session['username'], forum_posts=forum_posts)

if __name__ == '__main__':
    app.run(debug=True)