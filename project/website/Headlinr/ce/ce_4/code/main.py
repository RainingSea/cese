from flask import Flask, render_template, request, redirect, url_for
from nltk import sent_tokenize
from typing import List
import os

app = Flask(__name__)

class UserProfile:
    def __init__(self, username: str):
        self.username = username
        self.preferences = []

    def update_preferences(self, preferences: List[str]):
        self.preferences = preferences

    def get_preferences(self) -> List[str]:
        return self.preferences

class Article:
    def __init__(self, title: str, content: str, source: str):
        self.title = title
        self.content = content
        self.source = source

    def summarize(self) -> str:
        sentences = sent_tokenize(self.content)
        return ' '.join(sentences[:2])  # Return first two sentences as summary

class Bookmark:
    def __init__(self, article_title: str):
        self.article_title = article_title

class Headlinr:
    def __init__(self):
        self.users = []
        self.articles = []
        self.bookmarks = []
        self.load_data()

    def load_data(self):
        self.load_users()
        self.load_articles()
        self.load_bookmarks()

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, preferences = line.strip().split('|')
                    user = UserProfile(username)
                    user.update_preferences(preferences.split(','))
                    self.add_user(user)

    def load_articles(self):
        if os.path.exists('articles.txt'):
            with open('articles.txt', 'r') as f:
                for line in f:
                    title, content, source = line.strip().split('|')
                    article = Article(title, content, source)
                    self.add_article(article)

    def load_bookmarks(self):
        if os.path.exists('bookmarks.txt'):
            with open('bookmarks.txt', 'r') as f:
                for line in f:
                    article_title = line.strip()
                    bookmark = Bookmark(article_title)
                    self.bookmarks.append(bookmark)

    def add_user(self, user: UserProfile):
        self.users.append(user)

    def add_article(self, article: Article):
        self.articles.append(article)

    def bookmark_article(self, article_title: str):
        bookmark = Bookmark(article_title)
        self.bookmarks.append(bookmark)

    def generate_summaries(self) -> List[str]:
        return [article.summarize() for article in self.articles]

    def rank_articles(self) -> List[Article]:
        return sorted(self.articles, key=lambda x: x.title)  # Simple ranking by title

headlinr = Headlinr()

@app.route('/')
def index():
    summaries = headlinr.generate_summaries()
    return render_template('index.html', summaries=summaries)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        preferences = request.form.getlist('preferences')
        user = UserProfile(username)
        user.update_preferences(preferences)
        headlinr.add_user(user)
        return redirect(url_for('index'))
    return render_template('profile.html')

@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html', bookmarks=headlinr.bookmarks)

if __name__ == '__main__':
    app.run(port=8633, debug=False)
