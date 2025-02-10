from flask import Flask, render_template, request, redirect, url_for
from user_profile_manager import UserProfileManager
from article_manager import ArticleManager

app = Flask(__name__)
user_profile_manager = UserProfileManager()
article_manager = ArticleManager()

@app.route('/')
def index():
    return render_template('index.html', articles=article_manager.articles)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        user_id = request.form['user_id']
        preferences = request.form.getlist('preferences')
        user_profile_manager.add_user({'user_id': user_id, 'preferences': preferences})
        return redirect(url_for('index'))
    return render_template('profile.html', profiles=user_profile_manager.user_profiles)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_data = request.form['feedback']
        # Process feedback (e.g., save to a file or database)
        return redirect(url_for('index'))
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(port=8631, debug=False)
