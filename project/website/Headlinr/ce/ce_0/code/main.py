from flask import Flask, render_template, request, redirect, url_for
from search_engine import SearchEngine
from user_profile import UserProfile

app = Flask(__name__)
search_engine = SearchEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        new_preferences = request.form.getlist('preferences')
        search_engine.user_profile.update_preferences(new_preferences)
        return redirect(url_for('index'))
    return render_template('profile.html', preferences=search_engine.user_profile.get_preferences())

if __name__ == '__main__':
    app.run(port=8338, debug=False)
