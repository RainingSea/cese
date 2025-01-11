from flask import Flask, render_template, request, redirect, session
from DataManager import DataManager
from User import User
from Tip import Tip
from Article import Article
from ForumPost import ForumPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'
data_manager = DataManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = data_manager.load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tip = Tip(title, content)
        data_manager.save_tip(tip)
        return redirect('/tips')
    tips = data_manager.load_tips()
    return render_template('tips.html', tips=tips)

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        article = Article(title, content)
        data_manager.save_article(article)
        return redirect('/articles')
    articles = data_manager.load_articles()
    return render_template('articles.html', articles=articles)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        content = request.form['content']
        post = ForumPost(session['username'], content)
        data_manager.save_forum_post(post)
        return redirect('/forum')
    posts = data_manager.load_forum_posts()
    return render_template('forum.html', posts=posts)

if __name__ == '__main__':
    app.run(port=8370, debug=False)
