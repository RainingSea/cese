from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from tip import Tip
from forum_post import ForumPost
from article import Article  # Importing the Article class

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.authenticate():
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        tip_content = request.form['tip_content']
        tip = Tip(tip_content)
        tip.save()
        return redirect(url_for('tips'))

    tips_list = Tip.load_tips()
    return render_template('tips.html', tips=tips_list)

@app.route('/articles', methods=['GET', 'POST'])  # New route for articles
def articles():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        article_title = request.form['article_title']
        article_content = request.form['article_content']
        article = Article(article_title, article_content)
        article.save()
        return redirect(url_for('articles'))

    articles_list = Article.load_articles()
    return render_template('articles.html', articles=articles_list)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        post_content = request.form['post_content']
        forum_post = ForumPost(session['username'], post_content)
        forum_post.save()
        return redirect(url_for('forum'))

    posts_list = ForumPost.load_posts()
    return render_template('forum.html', posts=posts_list)

if __name__ == '__main__':
    app.run(debug=True)