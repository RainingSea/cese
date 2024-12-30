from flask import Flask, request, render_template, redirect, url_for
import os
from transformers import pipeline

app = Flask(__name__)

class UserProfile:
    def __init__(self, username: str):
        self.username = username
        self.topics = []
        self.sources = []
    
    def update_preferences(self, topics: list, sources: list):
        self.topics = topics
        self.sources = sources
        self.save_profile()

    def save_profile(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{','.join(self.topics)}|{','.join(self.sources)}\n")

    @staticmethod
    def load_profile(username: str):
        if not os.path.exists('users.txt'):
            return None
        with open('users.txt', 'r') as file:
            for line in file:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    profile = UserProfile(user_data[0])
                    profile.topics = user_data[1].split(',') if user_data[1] else []
                    profile.sources = user_data[2].split(',') if user_data[2] else []
                    return profile
        return None

class Article:
    def __init__(self, title: str, content: str, source: str):
        self.title = title
        self.content = content
        self.source = source

    def summarize(self) -> str:
        summarizer = pipeline("summarization")
        summary = summarizer(self.content, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']

class Bookmark:
    def __init__(self, username: str):
        self.username = username
        self.articles = []

    def add_bookmark(self, article: Article) -> None:
        self.articles.append(article)
        self.save_bookmarks()

    def remove_bookmark(self, article: Article) -> None:
        self.articles = [a for a in self.articles if a.title != article.title]
        self.save_bookmarks()

    def get_bookmarks(self) -> list:
        return self.articles

    def save_bookmarks(self) -> None:
        with open('bookmarks.txt', 'a') as file:
            for article in self.articles:
                file.write(f"{self.username}|{article.title}|{article.content}|{article.source}\n")

    @staticmethod
    def load_bookmarks(username: str) -> list:
        bookmarks = []
        if not os.path.exists('bookmarks.txt'):
            return bookmarks
        with open('bookmarks.txt', 'r') as file:
            for line in file:
                bookmark_data = line.strip().split('|')
                if bookmark_data[0] == username:
                    article = Article(bookmark_data[1], bookmark_data[2], bookmark_data[3])
                    bookmarks.append(article)
        return bookmarks

class NewsFeed:
    def __init__(self):
        self.articles = []

    def fetch_articles(self) -> list:
        if not os.path.exists('articles.txt'):
            return []
        with open('articles.txt', 'r') as file:
            for line in file:
                title, content, source = line.strip().split('|')
                article = Article(title, content, source)
                self.articles.append(article)
        return self.articles

    def rank_articles(self, user_profile: UserProfile) -> list:
        ranked_articles = []
        for article in self.articles:
            if any(topic in article.content for topic in user_profile.topics) or \
               any(source in article.source for source in user_profile.sources):
                ranked_articles.append(article)
        return ranked_articles

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        topics = request.form.getlist('topics')
        sources = request.form.getlist('sources')
        user_profile = UserProfile(username)
        user_profile.update_preferences(topics, sources)
        return redirect(url_for('index'))
    return render_template('profile.html')

@app.route('/articles', methods=['GET'])
def articles():
    username = request.args.get('username')
    user_profile = UserProfile.load_profile(username)
    news_feed = NewsFeed()
    articles = news_feed.fetch_articles()
    ranked_articles = news_feed.rank_articles(user_profile)
    summaries = {article.title: article.summarize() for article in ranked_articles}
    return render_template('article.html', summaries=summaries)

@app.route('/bookmark', methods=['POST'])
def bookmark():
    username = request.form['username']
    article_title = request.form['article_title']
    news_feed = NewsFeed()
    articles = news_feed.fetch_articles()
    article_to_bookmark = next((article for article in articles if article.title == article_title), None)
    if article_to_bookmark:
        bookmark = Bookmark(username)
        bookmark.add_bookmark(article_to_bookmark)
    return redirect(url_for('articles', username=username))

@app.route('/share', methods=['POST'])
def share():
    username = request.form['username']
    article_title = request.form['article_title']
    # Here you would implement the logic to share the article, e.g., through social media APIs
    # For now, we will just redirect to the articles page
    return redirect(url_for('articles', username=username))

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        username = request.form['username']
        feedback_text = request.form['feedback']
        with open('feedback.txt', 'a') as file:
            file.write(f"{username}|{feedback_text}\n")
        return redirect(url_for('index'))
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=True)