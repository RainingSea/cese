from flask import Flask, render_template, request, redirect, url_for
from UserProfileManager import UserProfileManager
from NewsSummaryGenerator import NewsSummaryGenerator
from BookmarkManager import BookmarkManager
from FeedbackManager import FeedbackManager

app = Flask(__name__)

user_profile_manager = UserProfileManager('users.txt')
news_summary_generator = NewsSummaryGenerator()
bookmark_manager = BookmarkManager('bookmarks.txt')
feedback_manager = FeedbackManager('feedback.txt')

@app.route('/')
def index():
    profiles = user_profile_manager.get_profiles()
    return render_template('index.html', profiles=profiles)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        user_data = request.form.to_dict()
        user_profile_manager.create_profile(user_data)
        return redirect(url_for('index'))
    return render_template('profile.html')

@app.route('/bookmarks')
def bookmarks():
    bookmarks = bookmark_manager.get_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        feedback_manager.submit_feedback(feedback_text)
        return redirect(url_for('index'))
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(port=9034, debug=False)
