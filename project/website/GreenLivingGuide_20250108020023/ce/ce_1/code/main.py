from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from tip import Tip
from article import Article
from forum_post import ForumPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

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
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        content = request.form['content']
        tip = Tip(content)
        tip.save()
    tips = load_tips()
    return render_template('tips.html', tips=tips)

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        article = Article(title, content)
        article.save()
    articles = load_articles()
    return render_template('articles.html', articles=articles)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        content = request.form['content']
        post = ForumPost(session['username'], content)
        post.save()
    posts = load_forum_posts()
    return render_template('forum.html', posts=posts)

if __name__ == '__main__':
    app.run(port=8306, debug=False)
