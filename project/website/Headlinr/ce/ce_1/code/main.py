from flask import Flask, render_template, request, redirect, url_for
from user_profile_manager import UserProfileManager
from news_feed import NewsFeed

app = Flask(__name__)
user_profile_manager = UserProfileManager()
news_feed = NewsFeed()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        user_id = request.form['user_id']
        preferences = request.form.getlist('preferences')
        user_profile_manager.update_profile(user_id, {"preferences": preferences})
        return redirect(url_for('profile'))
    return render_template('profile.html', profiles=user_profile_manager.user_profiles)

@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html')

if __name__ == '__main__':
    app.run(port=8630, debug=False)
