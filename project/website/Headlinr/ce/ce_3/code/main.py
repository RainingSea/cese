from flask import Flask, render_template, request, redirect, url_for
from user_manager import UserManager
from article_manager import ArticleManager
from summary_generator import SummaryGenerator
from ranking_system import RankingSystem

app = Flask(__name__)
user_manager = UserManager()
article_manager = ArticleManager()
summary_generator = SummaryGenerator()
ranking_system = RankingSystem()

@app.route('/')
def index():
    return render_template('index.html', articles=article_manager.articles)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        preferences = {'topics': request.form.getlist('preferences')}
        user_manager.create_user(username, preferences)
        return redirect(url_for('index'))
    return render_template('profile.html')

@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmark.html')

if __name__ == '__main__':
    app.run(port=8632, debug=False)
