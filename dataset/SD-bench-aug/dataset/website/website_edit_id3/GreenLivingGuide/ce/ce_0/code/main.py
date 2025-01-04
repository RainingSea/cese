from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from tip import Tip
from article import Article
from forum_post import ForumPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from the file
def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password, _ = line.strip().split('|')
            users.append(User(username, password))
    return users

# Load tips from the file
def load_tips():
    tips = []
    with open('tips.txt', 'r') as file:
        for line in file:
            content = line.strip()
            tips.append(Tip(content))
    return tips

# Load articles from the file
def load_articles():
    articles = []
    with open('articles.txt', 'r') as file:
        for line in file:
            title, content = line.strip().split('|')
            articles.append(Article(title, content))
    return articles

# Load forum posts from the file
def load_forum_posts():
    posts = []
    with open('forum.txt', 'r') as file:
        for line in file:
            username, content = line.strip().split('|')
            posts.append(ForumPost(username, content))
    return posts

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    user.save()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    tips = load_tips()
    articles = load_articles()
    return render_template('dashboard.html', tips=tips, articles=articles)

@app.route('/submit_tip', methods=['POST'])
def submit_tip():
    content = request.form['content']
    tip = Tip(content)
    tip.save()
    return redirect(url_for('dashboard'))

@app.route('/submit_article', methods=['POST'])
def submit_article():
    title = request.form['title']
    content = request.form['content']
    article = Article(title, content)
    article.save()
    return redirect(url_for('dashboard'))

@app.route('/forum')
def forum():
    posts = load_forum_posts()
    return render_template('forum.html', posts=posts)

@app.route('/submit_post', methods=['POST'])
def submit_post():
    username = request.form['username']
    content = request.form['content']
    post = ForumPost(username, content)
    post.save()
    return redirect(url_for('forum'))

if __name__ == '__main__':
    app.run(port=8131, debug=True)
