from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from article import Article
from social_share import SocialShare

app = Flask(__name__)
app.secret_key = 'your_secret_key'
social_share = SocialShare('users.txt', 'articles.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if social_share.register_user(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_bio = request.form['bio']
        social_share.update_user_bio(session['username'], new_bio)
    return render_template('profile.html', user=session['username'])

@app.route('/feed')
def feed():
    if 'username' not in session:
        return redirect(url_for('login'))
    articles = social_share.get_feed()
    return render_template('feed.html', articles=articles)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if social_share.login_user(username, password):
        session['username'] = username
        return redirect(url_for('feed'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8642, debug=False)
