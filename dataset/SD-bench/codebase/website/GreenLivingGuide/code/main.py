from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from tip import Tip
from article import Article
from forum_post import ForumPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key for production

# Load users, tips, articles, and forum posts at startup
users = User.load_users()
tips = Tip.load_tips()
articles = Article.load_articles()
forum_posts = ForumPost.load_forum_posts()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', tips=tips, articles=articles)

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
    posts = ForumPost.load_forum_posts()
    return render_template('forum.html', posts=posts)

@app.route('/submit_forum_post', methods=['POST'])
def submit_forum_post():
    username = request.form['username']
    content = request.form['content']
    post = ForumPost(username, content)
    post.save()
    return redirect(url_for('forum'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8307, debug=False)
