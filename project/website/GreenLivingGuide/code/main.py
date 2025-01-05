from flask import Flask, render_template, request, redirect, session
from data_manager import DataManager
from user import User
from tip import Tip
from article import Article
from forum_post import ForumPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'
data_manager = DataManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect('/')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = data_manager.load_users()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect('/dashboard')
    return 'Invalid credentials'

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        content = request.form['content']
        author = session['username']
        new_tip = Tip(content, author)
        data_manager.save_tip(new_tip)
        return redirect('/tips')
    tips = data_manager.load_tips()
    return render_template('tips.html', tips=tips)

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session['username']
        new_article = Article(title, content, author)
        data_manager.save_article(new_article)
        return redirect('/articles')
    articles = data_manager.load_articles()
    return render_template('articles.html', articles=articles)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        content = request.form['content']
        author = session['username']
        new_post = ForumPost(content, author)
        data_manager.save_forum_post(new_post)
        return redirect('/forum')
    posts = data_manager.load_forum_posts()
    return render_template('forum.html', posts=posts)

if __name__ == '__main__':
    app.run(port=8096, debug=False)
