from flask import Flask, render_template, request, redirect, url_for, flash
from UserManager import UserManager
from ArticleManager import ArticleManager
from CommentManager import CommentManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
article_manager = ArticleManager()
comment_manager = CommentManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        bio = request.form['bio']
        user = User(username, password, bio)
        user_manager.save_user(user)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        bio = request.form['bio']
        user_manager.update_user_bio(username, bio)
        flash('Profile updated successfully!', 'success')
    return render_template('profile.html')

@app.route('/feed')
def feed():
    articles = article_manager.articles
    return render_template('feed.html', articles=articles)

if __name__ == '__main__':
    user_manager.load_users()
    article_manager.load_articles()
    comment_manager.load_comments()
    app.run(port=8643, debug=False)
