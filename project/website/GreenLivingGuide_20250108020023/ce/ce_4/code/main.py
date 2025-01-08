from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from tip import Tip
from article import Article
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
            content = line.strip()
            tips.append(Tip(content))
    return tips

def load_articles():
    articles = []
    with open('articles.txt', 'r') as file:
        for line in file:
            title, content = line.strip().split('|')
            articles.append(Article(title, content))
    return articles

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
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        content = request.form['content']
        tip = Tip(content)
        with open('tips.txt', 'a') as file:
            file.write(f"{tip.content}\n")
    tips = load_tips()
    return render_template('tips.html', tips=tips)

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        article = Article(title, content)
        with open('articles.txt', 'a') as file:
            file.write(f"{article.title}|{article.content}\n")
    articles = load_articles()
    return render_template('articles.html', articles=articles)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        content = request.form['content']
        post = ForumPost(session.get('username'), content)
        with open('forum.txt', 'a') as file:
            file.write(f"{post.username}|{post.content}\n")
    forum_posts = load_forum_posts()
    return render_template('forum.html', posts=forum_posts)

if __name__ == '__main__':
    app.run(port=8309, debug=False)
