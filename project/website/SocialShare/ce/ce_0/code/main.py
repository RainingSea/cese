from flask import Flask, render_template, request, redirect, url_for
from UserManager import UserManager
from ArticleManager import ArticleManager

app = Flask(__name__)
user_manager = UserManager()
article_manager = ArticleManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    if request.method == 'POST':
        bio = request.form['bio']
        user_manager.update_profile(username, bio)
    return render_template('profile.html', user=username)

@app.route('/share_article', methods=['GET', 'POST'])
def share_article():
    if request.method == 'POST':
        username = request.form['username']
        content = request.form['content']
        article_manager.share_article(username, content)
        return redirect(url_for('discovery'))
    return render_template('content_share.html')

@app.route('/discovery')
def discovery():
    articles = article_manager.get_articles()
    return render_template('discovery.html', articles=articles)

if __name__ == '__main__':
    app.run(port=8418, debug=False)
