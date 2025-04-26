from flask import Flask, render_template, request, redirect, url_for
from nltk_processor import NLTKProcessor
from user_profile_manager import UserProfileManager
from bookmark_manager import BookmarkManager
from feedback_manager import FeedbackManager

app = Flask(__name__)

# Initialize managers
user_profile_manager = UserProfileManager('users.txt')
bookmark_manager = BookmarkManager('bookmarks.txt')
feedback_manager = FeedbackManager('feedback.txt')
nlp_processor = NLTKProcessor()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_profile_manager.validate_user(username, password):
            return redirect(url_for('main_page', username=username))
    return render_template('login.html')

@app.route('/home/<username>')
def main_page(username):
    articles = ["Article 1 content", "Article 2 content", "Article 3 content"]  # Example articles
    summaries = [nlp_processor.summarize(article) for article in articles]
    return render_template('main_page.html', username=username, summaries=summaries)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        preferences = request.form['preferences']
        user_profile_manager.update_profile(username, preferences)
        return redirect(url_for('profile'))
    return render_template('profile.html')

@app.route('/bookmarks', methods=['GET', 'POST'])
def bookmarks():
    if request.method == 'POST':
        article_id = request.form['article_id']
        bookmark_manager.add_bookmark(article_id)
        return redirect(url_for('bookmarks'))
    
    bookmarks = bookmark_manager.list_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/feedback', methods=['POST'])
def feedback():
    feedback_text = request.form['feedback']
    feedback_manager.submit_feedback(feedback_text)
    return redirect(url_for('main_page', username=request.args.get('username')))

if __name__ == '__main__':
    app.run(port=8178, debug=False)
