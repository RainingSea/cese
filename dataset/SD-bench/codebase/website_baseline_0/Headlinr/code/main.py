from flask import Flask, render_template, request, redirect, url_for
from transformers import pipeline
import os
import json

app = Flask(__name__)

class UserProfile:
    def __init__(self, username: str):
        self.username = username
        self.preferences = self.fetch_profile(username)

    def create_profile(self, username: str) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{username}\n")

    def update_preferences(self, preferences: dict) -> None:
        with open('preferences.txt', 'a') as f:
            f.write(f"{self.username}|{json.dumps(preferences)}\n")

    def fetch_profile(self, username: str) -> dict:
        with open('users.txt', 'r') as f:
            users = f.readlines()
            for user in users:
                if user.strip() == username:
                    return {"username": username, "preferences": {}}
        return {}

class Article:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.summary = self.generate_summary()

    def generate_summary(self) -> str:
        summarizer = pipeline("summarization")
        summary = summarizer(self.content, max_length=50, min_length=25, do_sample=False)
        return summary[0]['summary_text']

class Bookmark:
    def __init__(self, user: str):
        self.user = user

    def add_bookmark(self, article_title: str) -> None:
        with open('bookmarks.txt', 'a') as f:
            f.write(f"{self.user}|{article_title}\n")

    def fetch_bookmarks(self) -> list:
        bookmarks = []
        with open('bookmarks.txt', 'r') as f:
            for line in f:
                if line.startswith(self.user):
                    bookmarks.append(line.strip().split('|')[1])
        return bookmarks

class Feedback:
    def __init__(self, user: str, comments: str):
        self.user = user
        self.comments = comments

    def submit_feedback(self) -> None:
        with open('feedback.txt', 'a') as f:
            f.write(f"{self.user}|{self.comments}\n")

class ArticleManager:
    def __init__(self):
        self.articles = self.load_articles()

    def load_articles(self) -> list:
        articles = []
        with open('articles.txt', 'r') as f:
            for line in f:
                title, content = line.strip().split('|')
                articles.append(Article(title, content))
        return articles

    def rank_articles(self) -> list:
        # Placeholder for ranking logic, currently returns articles as is
        return self.articles

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        preferences = request.form.getlist('preferences')
        user = UserProfile(username)
        user.create_profile(username)
        user.update_preferences({"topics": preferences})
        return redirect(url_for('index'))
    return render_template('profile.html')

@app.route('/bookmarks')
def bookmarks():
    user = request.args.get('user', 'guest')
    bookmark = Bookmark(user)
    user_bookmarks = bookmark.fetch_bookmarks()
    return render_template('bookmarks.html', bookmarks=user_bookmarks)

@app.route('/articles')
def articles():
    article_manager = ArticleManager()
    articles_list = article_manager.rank_articles()
    return render_template('articles.html', articles=[{"title": article.title, "summary": article.summary} for article in articles_list])

@app.route('/feedback', methods=['POST'])
def feedback():
    user = request.form['username']
    comments = request.form['comments']
    feedback = Feedback(user, comments)
    feedback.submit_feedback()
    return redirect(url_for('index'))

@app.route('/share_article', methods=['POST'])
def share_article():
    article_title = request.form['article_title']
    # Logic to share the article (e.g., generating a link) would go here
    return redirect(url_for('articles'))

if __name__ == '__main__':
    app.run(port=8536, debug=False)
