from flask import Flask, render_template, request, redirect, url_for
from user_manager import UserManager
from news_manager import NewsManager

app = Flask(__name__)
user_manager = UserManager()
news_manager = NewsManager()

@app.route('/')
def index():
    articles = news_manager.rank_articles(user_manager.get_user_preferences())
    return render_template('index.html', articles=articles)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        preferences = request.form.getlist('preferences')
        user_manager.create_user(username, preferences)
        return redirect(url_for('index'))
    return render_template('profile.html')

@app.route('/bookmarks')
def bookmarks():
    bookmarked_articles = user_manager.get_bookmarked_articles()
    return render_template('bookmarks.html', bookmarks=bookmarked_articles)

if __name__ == '__main__':
    user_manager.load_users()
    news_manager.load_articles()
    app.run(port=8629, debug=False)
