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

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    articles = load_articles()
    return render_template('home.html', articles=articles)

@app.route('/submit_tip', methods=['GET', 'POST'])
def submit_tip():
    if request.method == 'POST':
        content = request.form['content']
        tip = Tip(content)
        tip.save()
        return redirect(url_for('home'))
    return render_template('tips.html')

@app.route('/articles')
def articles():
    articles = load_articles()
    return render_template('articles.html', articles=articles)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        username = request.form['username']
        content = request.form['content']
        post = ForumPost(username, content)
        post.save()
        return redirect(url_for('forum'))
    posts = load_forum_posts()
    return render_template('forum.html', posts=posts)

if __name__ == '__main__':
    app.run(port=8954, debug=False)
