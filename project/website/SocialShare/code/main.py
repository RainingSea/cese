from flask import Flask, request, redirect, url_for, session, render_template
from UserManager import UserManager
from ArticleManager import ArticleManager
from CommentManager import CommentManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
article_manager = ArticleManager('articles.txt')
comment_manager = CommentManager('comments.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    bio = request.form['bio']
    try:
        user_manager.register_user(username, password, bio)
        return redirect(url_for('login'))
    except ValueError as e:
        return str(e)

@app.route('/do_login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    try:
        user = user_manager.login_user(username, password)
        session['username'] = user.username
        return redirect(url_for('feed'))  # Redirect to feed after successful login
    except ValueError as e:
        return str(e)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        new_password = request.form['new_password']
        new_bio = request.form['new_bio']
        try:
            user_manager.update_user_profile(session['username'], new_password, new_bio)
            return redirect(url_for('profile'))
        except ValueError as e:
            return str(e)
    return render_template('profile.html', username=session.get('username'))

@app.route('/feed')
def feed():
    articles = article_manager.get_articles()
    return render_template('feed.html', articles=articles)

@app.route('/upload', methods=['POST'])
def upload():
    title = request.form['title']
    content = request.form['content']
    author = session.get('username')
    article_manager.add_article(title, content, author)
    return redirect(url_for('feed'))

@app.route('/comment', methods=['POST'])
def comment():
    article_id = request.form['article_id']
    author = session.get('username')
    content = request.form['content']
    comment_manager.add_comment(article_id, author, content)
    return redirect(url_for('feed'))

if __name__ == '__main__':
    app.run(port=8646, debug=False)
