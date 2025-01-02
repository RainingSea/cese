from flask import Flask, render_template, request, redirect, url_for, session
import os
from user import User
from tip import Tip
from article import Article
from forum_post import ForumPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from the users.txt file
def load_users():
    users = []
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password, _ = line.strip().split('|')
                users.append(User(username, password))
    return users

# Load tips from the tips.txt file
def load_tips():
    return Tip.load_all()

# Load articles from the articles.txt file
def load_articles():
    return Article.load_all()

# Load forum posts from the forum.txt file
def load_forum_posts():
    return ForumPost.load_all()

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
    if 'username' not in session:
        return redirect(url_for('login'))
    articles = load_articles()
    tips = load_tips()
    return render_template('dashboard.html', articles=articles, tips=tips)

@app.route('/submit_tip', methods=['POST'])
def submit_tip():
    if 'username' not in session:
        return redirect(url_for('login'))
    content = request.form['content']
    tip = Tip(content)
    tip.save()
    return redirect(url_for('tips'))

@app.route('/tips')
def tips():
    if 'username' not in session:
        return redirect(url_for('login'))
    tips = load_tips()
    return render_template('tips.html', tips=tips)

@app.route('/submit_article', methods=['POST'])
def submit_article():
    if 'username' not in session:
        return redirect(url_for('login'))
    title = request.form['title']
    content = request.form['content']
    article = Article(title, content)
    article.save()
    return redirect(url_for('articles'))

@app.route('/articles')
def articles():
    if 'username' not in session:
        return redirect(url_for('login'))
    articles = load_articles()
    return render_template('articles.html', articles=articles)

@app.route('/forum')
def forum():
    if 'username' not in session:
        return redirect(url_for('login'))
    forum_posts = load_forum_posts()
    return render_template('forum.html', forum_posts=forum_posts)

@app.route('/submit_forum_post', methods=['POST'])
def submit_forum_post():
    if 'username' not in session:
        return redirect(url_for('login'))
    content = request.form['content']
    forum_post = ForumPost(session['username'], content)
    forum_post.save()
    return redirect(url_for('forum'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8171, debug=True)
