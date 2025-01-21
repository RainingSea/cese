from flask import Flask, render_template, request, redirect, url_for
from UserProfileManager import UserProfileManager
from NewsArticleManager import NewsArticleManager
from BookmarkManager import BookmarkManager

app = Flask(__name__)

user_profile_manager = UserProfileManager()
news_article_manager = NewsArticleManager()
bookmark_manager = BookmarkManager()

@app.route('/')
def index():
    articles = news_article_manager.articles
    summaries = [news_article_manager.summarize_article(article) for article in articles]
    return render_template('index.html', summaries=summaries)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_profile_manager.save_user({'username': username, 'password': password, 'preferences': {}})
        return redirect(url_for('index'))
    return render_template('profile.html')

@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html', bookmarks=bookmark_manager.bookmarks)

if __name__ == '__main__':
    app.run(port=9037, debug=False)
