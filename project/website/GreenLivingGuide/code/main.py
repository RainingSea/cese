from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from tip_manager import TipManager
from article_manager import ArticleManager
from forum_manager import ForumManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
tip_manager = TipManager()
article_manager = ArticleManager()
forum_manager = ForumManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.validate_user(username, password):
            session['username'] = username
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in user_manager.users:
            return "Username already exists.", 400
        user_manager.add_user(username, password)
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Display the dashboard with tips and articles."""
    if 'username' not in session:
        return redirect('/')
    tips = tip_manager.get_tips()
    articles = article_manager.get_articles()
    return render_template('dashboard.html', tips=tips, articles=articles)

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    """Handle tips submission and display."""
    if request.method == 'POST':
        tip = request.form['tip']
        tip_manager.add_tip(tip)
        if not tip_manager.verify_tip_data():
            return "Error saving tip data.", 500
        return redirect('/tips')
    tips = tip_manager.get_tips()
    return render_template('tips.html', tips=tips)

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    """Handle articles submission and display."""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        article = f"{title}: {content}"
        article_manager.add_article(article)
        if not article_manager.verify_article_data():
            return "Error saving article data.", 500
        return redirect('/articles')
    articles = article_manager.get_articles()
    return render_template('articles.html', articles=articles)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    """Handle forum posts submission and display."""
    if request.method == 'POST':
        content = request.form['content']
        post = f"{session['username']}: {content}"
        forum_manager.add_post(post)
        if not forum_manager.verify_post_data():
            return "Error saving post data.", 500
        return redirect('/forum')
    posts = forum_manager.get_posts()
    return render_template('forum.html', posts=posts)

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8372, debug=False)
