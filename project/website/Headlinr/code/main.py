from flask import Flask, render_template, request, redirect, url_for, flash
from UserProfileManager import UserProfileManager
from NewsManager import NewsManager
from BookmarkManager import BookmarkManager
from FeedbackManager import FeedbackManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

user_profile_manager = UserProfileManager('users.txt')
news_manager = NewsManager('articles.txt')
bookmark_manager = BookmarkManager('bookmarks.txt')
feedback_manager = FeedbackManager('feedback.txt')

@app.route('/')
def index():
    articles = news_manager.load_articles()
    ranked_articles = news_manager.rank_articles(user_profile_manager.get_user_preferences())
    return render_template('index.html', articles=ranked_articles)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        preferences = request.form.getlist('preferences')
        user_profile_manager.create_user(username, {'preferences': preferences})
        flash('User profile created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('profile.html')

@app.route('/article/<int:article_id>')
def article(article_id):
    articles = news_manager.load_articles()
    if 0 <= article_id < len(articles):
        article = articles[article_id]
        return render_template('article.html', article=article)
    flash('Article not found!', 'error')
    return redirect(url_for('index'))

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    user = request.form['user']
    feedback = request.form['feedback']
    feedback_manager.submit_feedback(user, feedback)
    flash('Feedback submitted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/summarize', methods=['POST'])
def summarize_article():
    article_id = int(request.form['article_id'])
    articles = news_manager.load_articles()
    if 0 <= article_id < len(articles):
        article = articles[article_id]
        summary = news_manager.generate_summary(article['content'])
        return render_template('summary.html', article=article, summary=summary)
    flash('Article not found for summarization!', 'error')
    return redirect(url_for('index'))

@app.route('/share/<int:article_id>')
def share_article(article_id):
    articles = news_manager.load_articles()
    if 0 <= article_id < len(articles):
        article = articles[article_id]
        return render_template('share.html', article=article)
    flash('Article not found for sharing!', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=9039, debug=False)
