from flask import Flask, render_template, request, redirect, url_for
from search_engine import SearchEngine
from user_profile import UserProfile
from bookmark_manager import BookmarkManager

app = Flask(__name__)

class Main:
    def __init__(self):
        self.search_engine = SearchEngine()
        self.user_profile = UserProfile()
        self.bookmark_manager = BookmarkManager()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        if request.method == 'POST':
            preferences = request.form.get('preferences')
            self.user_profile.save_profile(preferences)
            return redirect(url_for('index'))
        return render_template('profile.html', preferences=self.user_profile.load_profile())

    @app.route('/news')
    def news():
        query = request.args.get('query', '')
        articles = self.search_engine.search(query)
        return render_template('news.html', articles=articles)

if __name__ == '__main__':
    main_app = Main()
    app.run(port=8339, debug=False)
