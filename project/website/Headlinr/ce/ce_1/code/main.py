from flask import Flask, render_template, request, redirect, url_for
from user_profile_manager import UserProfileManager
from news_article_manager import NewsArticleManager

app = Flask(__name__)

user_profile_manager = UserProfileManager()
news_article_manager = NewsArticleManager()

@app.route('/')
def index():
    return render_template('index.html', articles=news_article_manager.rank_articles([]))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        preferences = request.form.getlist('preferences')
        user_profile_manager.create_profile(username, preferences)
        return redirect(url_for('index'))
    return render_template('profile.html', profiles=user_profile_manager.profiles)

@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html', bookmarks=user_profile_manager.get_profile('default_user').bookmarks)

if __name__ == '__main__':
    app.run(port=9035, debug=False)
