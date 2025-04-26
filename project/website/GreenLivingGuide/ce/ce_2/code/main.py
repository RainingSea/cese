from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from user_manager import UserManager
from content_manager import ContentManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

user_manager = UserManager()
content_manager = ContentManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/home')
        else:
            return "Login Failed"
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        tip = request.form['tip']
        content_manager.submit_tip(tip)
        return redirect('/tips')
    tips = content_manager.get_tips()
    return render_template('tips.html', tips=tips)

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        article = request.form['article']
        content_manager.submit_article(article)
        return redirect('/articles')
    articles = content_manager.get_recent_articles()
    return render_template('articles.html', articles=articles)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        post = request.form['post']
        content_manager.post_to_forum(post)
        return redirect('/forum')
    forum_posts = content_manager.get_forum_posts()
    return render_template('forum.html', posts=forum_posts)

if __name__ == '__main__':
    app.run(port=8173, debug=False)
