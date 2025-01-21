from flask import Flask, render_template, request, redirect, session
from DataManager import DataManager
from User import User
from Tip import Tip
from Article import Article
from ForumPost import ForumPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'
data_manager = DataManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        tips = data_manager.load_tips()
        articles = data_manager.load_articles()
        return render_template('dashboard.html', username=session['username'], tips=tips, articles=articles)
    return redirect('/')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = data_manager.load_users()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect('/dashboard')
    return redirect('/')

@app.route('/submit_tip', methods=['POST'])
def submit_tip():
    if 'username' in session:
        content = request.form['content']
        tip = Tip(content)
        data_manager.save_tip(tip)
        return redirect('/dashboard')
    return redirect('/')

@app.route('/submit_article', methods=['POST'])
def submit_article():
    if 'username' in session:
        title = request.form['title']
        content = request.form['content']
        article = Article(title, content)
        data_manager.save_article(article)
        return redirect('/dashboard')
    return redirect('/')

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        if 'username' in session:
            content = request.form['content']
            post = ForumPost(session['username'], content)
            data_manager.save_forum_post(post)
            return redirect('/forum')
    posts = data_manager.load_forum_posts()
    return render_template('forum.html', posts=posts)

if __name__ == '__main__':
    app.run(port=8951, debug=False)
