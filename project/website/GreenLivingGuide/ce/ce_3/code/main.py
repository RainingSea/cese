from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from tip import Tip
from article import Article
from forum_post import ForumPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from file
def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

# Load tips from file
def load_tips():
    tips = []
    with open('tips.txt', 'r') as file:
        for line in file:
            tips.append(Tip(line.strip()))
    return tips

# Load articles from file
def load_articles():
    articles = []
    with open('articles.txt', 'r') as file:
        for line in file:
            title, content = line.strip().split('|')
            articles.append(Article(title, content))
    return articles

# Load forum posts from file
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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', tips=load_tips(), articles=load_articles())

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        new_tip = Tip(request.form['tip_content'])
        new_tip.save()
        return redirect(url_for('tips'))
    return render_template('tips.html', tips=load_tips())

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        new_article = Article(request.form['title'], request.form['content'])
        new_article.save()
        return redirect(url_for('articles'))
    return render_template('articles.html', articles=load_articles())

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        new_post = ForumPost(request.form['username'], request.form['content'])
        new_post.save()
        return redirect(url_for('forum'))
    return render_template('forum.html', posts=load_forum_posts())

if __name__ == '__main__':
    app.run(port=8953, debug=False)
