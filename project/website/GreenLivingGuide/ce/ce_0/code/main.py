from flask import Flask, render_template, request, redirect, session
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
            content, author = line.strip().split('|')
            tips.append(Tip(content, author))
    return tips

def load_articles():
    articles = []
    with open('articles.txt', 'r') as file:
        for line in file:
            title, content, author = line.strip().split('|')
            articles.append(Article(title, content, author))
    return articles

def load_forum_posts():
    forum_posts = []
    with open('forum.txt', 'r') as file:
        for line in file:
            content, author = line.strip().split('|')
            forum_posts.append(ForumPost(content, author))
    return forum_posts

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    user.save()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    articles = load_articles()
    tips = load_tips()
    return render_template('dashboard.html', articles=articles, tips=tips)

@app.route('/tips')
def tips():
    tips = load_tips()
    return render_template('tips.html', tips=tips)

@app.route('/articles')
def articles():
    articles = load_articles()
    return render_template('articles.html', articles=articles)

@app.route('/forum')
def forum():
    forum_posts = load_forum_posts()
    return render_template('forum.html', forum_posts=forum_posts)

if __name__ == '__main__':
    app.run(port=8950, debug=False)
