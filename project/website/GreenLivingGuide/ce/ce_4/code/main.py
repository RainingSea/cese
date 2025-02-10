from flask import Flask, render_template, request, redirect, session
from UserManager import UserManager
from TipManager import TipManager
from ArticleManager import ArticleManager
from ForumManager import ForumManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'

user_manager = UserManager('users.txt')
tip_manager = TipManager('tips.txt')
article_manager = ArticleManager('articles.txt')
forum_manager = ForumManager('forum_posts.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/dashboard')
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    tips = tip_manager.tips
    articles = article_manager.articles
    return render_template('dashboard.html', tips=tips, articles=articles)

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        tip = request.form['tip']
        tip_manager.submit_tip(tip)
        return redirect('/tips')
    return render_template('tips.html', tips=tip_manager.tips)

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        article = request.form['article']
        article_manager.submit_article(article)
        return redirect('/articles')
    return render_template('articles.html', articles=article_manager.articles)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        post = request.form['post']
        forum_manager.submit_post(post)
        return redirect('/forum')
    return render_template('forum.html', posts=forum_manager.posts)

if __name__ == '__main__':
    app.run(port=8545, debug=False)
