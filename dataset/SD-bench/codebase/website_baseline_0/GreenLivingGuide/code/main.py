from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from tip import Tip
from article import Article
from forum_post import ForumPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    except FileNotFoundError:
        pass  # Handle the case where the file does not exist
    return users

def load_tips():
    tips = []
    try:
        with open('tips.txt', 'r') as file:
            for line in file:
                content = line.strip()
                tips.append(Tip(content))
    except FileNotFoundError:
        pass  # Handle the case where the file does not exist
    return tips

def load_articles():
    articles = []
    try:
        with open('articles.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                articles.append(Article(title, content))
    except FileNotFoundError:
        pass  # Handle the case where the file does not exist
    return articles

def load_forum_posts():
    forum_posts = []
    try:
        with open('forum.txt', 'r') as file:
            for line in file:
                username, content = line.strip().split('|')
                forum_posts.append(ForumPost(username, content))
    except FileNotFoundError:
        pass  # Handle the case where the file does not exist
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
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', tips=load_tips(), articles=load_articles())

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
    return render_template('forum.html', posts=load_forum_posts())

@app.route('/submit_forum_post', methods=['POST'])
def submit_forum_post():
    username = request.form['username']
    content = request.form['content']
    post = ForumPost(username, content)
    post.save()
    return redirect(url_for('forum'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8535, debug=False)
