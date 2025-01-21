from flask import Flask, render_template, request, redirect, url_for
from user_manager import UserManager
from news_manager import NewsManager

app = Flask(__name__)
user_manager = UserManager()
news_manager = NewsManager()

@app.route('/')
def index():
    return render_template('index.html', articles=news_manager.articles)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        preferences = request.form.get('preferences', {})
        user_manager.add_user(username, preferences)
        return redirect(url_for('index'))
    return render_template('profile.html', users=user_manager.users)

@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html', bookmarks=news_manager.get_bookmarks())

if __name__ == '__main__':
    app.run(port=9036, debug=False)
