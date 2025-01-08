from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from tip import Tip
from article import Article
from forum_post import ForumPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    with open('users.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_tips():
    tips = []
    with open('tips.txt', 'r') as f:
        for line in f:
            content = line.strip()
            tips.append(Tip(content))
    return tips

def load_articles():
    articles = []
    with open('articles.txt', 'r') as f:
        for line in f:
            title, content = line.strip().split('|')
            articles.append(Article(title, content))
    return articles

def load_forum_posts():
    posts = []
    with open('forum.txt', 'r') as f:
        for line in f:
            username, content = line.strip().split('|')
            posts.append(ForumPost(username, content))
    return posts

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        tip_content = request.form['tip']
        tip = Tip(tip_content)
        with open('tips.txt', 'a') as f:
            f.write(f"{tip.content}\n")
        return redirect(url_for('tips'))
    return render_template('tips.html', tips=load_tips())

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        article = Article(title, content)
        with open('articles.txt', 'a') as f:
            f.write(f"{article.title}|{article.content}\n")
        return redirect(url_for('articles'))
    return render_template('articles.html', articles=load_articles())

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        username = session['username']
        content = request.form['content']
        post = ForumPost(username, content)
        with open('forum.txt', 'a') as f:
            f.write(f"{post.username}|{post.content}\n")
        return redirect(url_for('forum'))
    return render_template('forum.html', posts=load_forum_posts())

if __name__ == '__main__':
    app.run(port=8308, debug=False)
