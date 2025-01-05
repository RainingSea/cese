from flask import Flask, render_template, request, redirect, url_for, session
from data_manager import DataManager, User

app = Flask(__name__)
app.secret_key = 'your_secret_key'
data_manager = DataManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
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
    return 'Invalid credentials', 401

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        content = request.form['content']
        author = session['username']
        tip = Tip(content, author)
        data_manager.save_tip(tip)
        return redirect(url_for('tips'))
    tips = data_manager.load_tips()
    return render_template('tips.html', tips=tips)

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session['username']
        article = Article(title, content, author)
        data_manager.save_article(article)
        return redirect(url_for('articles'))
    articles = data_manager.load_articles()
    return render_template('articles.html', articles=articles)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        content = request.form['content']
        author = session['username']
        post = ForumPost(content, author)
        data_manager.save_forum_post(post)
        return redirect(url_for('forum'))
    posts = data_manager.load_forum_posts()
    return render_template('forum.html', posts=posts)

if __name__ == '__main__':
    app.run(port=8094, debug=False)
