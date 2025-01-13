from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from tip import Tip
from article import Article
from forum_post import ForumPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from the file
def load_users():
    return User.load_all()

# Load tips from the file
def load_tips():
    return Tip.load_all()

# Load articles from the file
def load_articles():
    return Article.load_all()

# Load forum posts from the file
def load_forum_posts():
    return ForumPost.load_all()

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
    if 'username' not in session:
        return redirect(url_for('login'))
    tips = load_tips()
    articles = load_articles()
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
    if 'username' not in session:
        return redirect(url_for('login'))
    forum_posts = load_forum_posts()
    return render_template('forum.html', forum_posts=forum_posts)

@app.route('/post_forum', methods=['POST'])
def post_forum():
    username = session['username']  # Use session username
    content = request.form['content']
    forum_post = ForumPost(username, content)
    forum_post.save()
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
    app.run(port=8070, debug=False)
