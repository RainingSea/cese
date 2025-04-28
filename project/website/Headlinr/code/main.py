from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserProfile:
    def __init__(self, username, preferences):
        self.username = username
        self.preferences = preferences

    def create_profile(self):
        with open('preferences.txt', 'a') as f:
            f.write(f"{self.username}|{','.join(self.preferences)}\n")

    def update_preferences(self, preferences):
        self.preferences = preferences
        self._update_preferences_file()

    def _update_preferences_file(self):
        lines = []
        with open('preferences.txt', 'r') as f:
            lines = f.readlines()
        
        with open('preferences.txt', 'w') as f:
            for line in lines:
                if line.startswith(self.username):
                    f.write(f"{self.username}|{','.join(self.preferences)}\n")
                else:
                    f.write(line)

class BookmarkManager:
    def __init__(self):
        self.bookmarks = self.load_bookmarks()

    def load_bookmarks(self):
        if os.path.exists('bookmarks.txt'):
            with open('bookmarks.txt', 'r') as f:
                return [line.strip() for line in f.readlines()]
        return []

    def add_bookmark(self, article_id):
        self.bookmarks.append(article_id)
        with open('bookmarks.txt', 'a') as f:
            f.write(f"{article_id}\n")

    def remove_bookmark(self, article_id):
        if article_id in self.bookmarks:
            self.bookmarks.remove(article_id)
            with open('bookmarks.txt', 'w') as f:
                f.writelines(f"{bm}\n" for bm in self.bookmarks)

    def get_bookmarks(self):
        return self.bookmarks

class SearchEngine:
    def search(self, query):
        # Dummy search implementation
        return [f"Article related to {query}"]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simple authentication (not secure)
        if username and password:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_profile = UserProfile(session['username'], [])
    if request.method == 'POST':
        preferences = request.form.get('preferences').split(',')
        user_profile.update_preferences(preferences)
        return redirect(url_for('index'))
    
    return render_template('profile.html')

@app.route('/news')
def news():
    search_engine = SearchEngine()
    results = search_engine.search("latest news")
    return render_template('news.html', results=results)

if __name__ == '__main__':
    app.run(port=8341, debug=False)
