from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from article_manager import ArticleManager
from tip_manager import TipManager
from forum_manager import ForumManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
article_manager = ArticleManager()
tip_manager = TipManager()
forum_manager = ForumManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    recent_articles = article_manager.get_recent_articles()
    return render_template('dashboard.html', articles=recent_articles)

@app.route('/submit_article', methods=['GET', 'POST'])
def submit_article():
    if request.method == 'POST':
        article = request.form['article']
        article_manager.submit_article(article)
        return redirect(url_for('dashboard'))
    return render_template('article_submission.html')

@app.route('/submit_tip', methods=['GET', 'POST'])
def submit_tip():
    if request.method == 'POST':
        tip = request.form['tip']
        tip_manager.submit_tip(tip)
        return redirect(url_for('dashboard'))
    return render_template('tip_submission.html')

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        post = request.form['post']
        forum_manager.submit_post(post)
        return redirect(url_for('forum'))
    posts = forum_manager.get_posts()
    return render_template('forum.html', posts=posts)

if __name__ == '__main__':
    app.run(port=8334, debug=False)
