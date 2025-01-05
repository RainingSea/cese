from flask import Flask, render_template, request, redirect, url_for, session
from typing import List
from data_manager import DataManager
from models import User, Tip, Article, ForumPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key
data_manager = DataManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        tips = data_manager.load_tips()
        articles = data_manager.load_articles()
        return render_template('dashboard.html', tips=tips, articles=articles)
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = data_manager.load_users()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/submit_tip', methods=['POST'])
def submit_tip():
    if 'username' in session:
        content = request.form['content']
        tip = Tip(content=content, author=session['username'])
        data_manager.save_tip(tip)
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/articles')
def articles():
    if 'username' in session:
        articles = data_manager.load_articles()
        return render_template('articles.html', articles=articles)
    return redirect(url_for('login'))

@app.route('/submit_article', methods=['POST'])
def submit_article():
    if 'username' in session:
        title = request.form['title']
        content = request.form['content']
        article = Article(title=title, content=content, author=session['username'])
        data_manager.save_article(article)
        return redirect(url_for('articles'))
    return redirect(url_for('login'))

@app.route('/forum')
def forum():
    if 'username' in session:
        posts = data_manager.load_forum_posts()
        return render_template('forum.html', posts=posts)
    return redirect(url_for('login'))

@app.route('/submit_forum_post', methods=['POST'])
def submit_forum_post():
    if 'username' in session:
        content = request.form['content']
        post = ForumPost(content=content, author=session['username'])
        data_manager.save_forum_post(post)
        return redirect(url_for('forum'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8095, debug=False)
