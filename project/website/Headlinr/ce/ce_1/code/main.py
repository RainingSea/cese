from flask import Flask, render_template, request, redirect, url_for
from tools import load_user_profiles, load_articles, UserProfile, SearchEngine

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        preferences = request.form.to_dict()
        user_profile = UserProfile()
        user_profile.save_profile(preferences)
        return redirect(url_for('news'))
    return render_template('profile.html')

@app.route('/news')
def news():
    user_profile = UserProfile()
    preferences = user_profile.load_profile()
    articles = load_articles()
    search_engine = SearchEngine()
    ranked_articles = search_engine.rank_articles(articles)
    return render_template('news.html', articles=ranked_articles)

@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        # Handle feedback submission
        return redirect(url_for('news'))
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(port=8176, debug=False)
