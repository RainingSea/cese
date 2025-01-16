from flask import Flask, render_template, request, redirect, url_for, session
from SocialShare import SocialShare

app = Flask(__name__)
app.secret_key = 'your_secret_key'
social_share = SocialShare('users.txt', 'articles.txt', 'comments.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        bio = request.form['bio']
        social_share.register_user(username, password, bio)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if social_share.login_user(username, password):
        session['username'] = username
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = social_share.get_user_profile(session['username'])
    return render_template('profile.html', user=user)

@app.route('/feed')
def feed():
    if 'username' not in session:
        return redirect(url_for('login'))
    articles = social_share.get_feed()
    return render_template('feed.html', articles=articles)

@app.route('/discovery')
def discovery():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('discovery.html')

if __name__ == '__main__':
    app.run(port=8645, debug=False)
