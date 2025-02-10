from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from tip import Tip
from article import Article
from forum_post import ForumPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.load_all()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        tip_content = request.form['tip']
        new_tip = Tip(tip_content)
        new_tip.save()
    tips_list = Tip.load_all()
    return render_template('tips.html', tips=tips_list)

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_article = Article(title, content)
        new_article.save()
    articles_list = Article.load_all()
    return render_template('articles.html', articles=articles_list)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        username = session.get('username')
        message = request.form['message']
        new_post = ForumPost(username, message)
        new_post.save()
    posts = ForumPost.load_all()
    return render_template('forum.html', posts=posts)

if __name__ == '__main__':
    app.run(port=8543, debug=False)
