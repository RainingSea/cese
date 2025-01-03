from flask import Flask, render_template, request, redirect, url_for, flash
from user import User
from tip import Tip
from article import Article
from forum_post import ForumPost  # Import the ForumPost class

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.authenticate():
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        tip_content = request.form['tip_content']
        new_tip = Tip(tip_content)
        new_tip.save()
        flash('Tip submitted successfully!')
        return redirect(url_for('tips'))
    
    tips_list = Tip.load_tips()
    return render_template('tips.html', tips=tips_list)

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        article_title = request.form['article_title']
        article_content = request.form['article_content']
        new_article = Article(article_title, article_content)
        new_article.save()
        flash('Article submitted successfully!')
        return redirect(url_for('articles'))
    
    articles_list = Article.load_articles()
    return render_template('articles.html', articles=articles_list)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        username = request.form['username']
        post_content = request.form['post_content']
        new_post = ForumPost(username, post_content)
        new_post.save()
        flash('Post submitted successfully!')
        return redirect(url_for('forum'))
    
    posts_list = ForumPost.load_posts()
    return render_template('forum.html', posts=posts_list)

if __name__ == '__main__':
    app.run(debug=True)