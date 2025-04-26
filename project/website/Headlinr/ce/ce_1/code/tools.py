import nltk
import json

class UserProfile:
    def __init__(self, filename='users.txt'):
        self.filename = filename
        self.preferences = {}

    def load_profile(self):
        try:
            with open(self.filename, 'r') as file:
                data = file.read().strip().split('|')
                self.preferences = {item.split(':')[0]: item.split(':')[1] for item in data}
        except FileNotFoundError:
            self.preferences = {}
        return self.preferences

    def save_profile(self, preferences):
        with open(self.filename, 'w') as file:
            file.write('|'.join([f"{key}:{value}" for key, value in preferences.items()]))

class Article:
    def __init__(self, content):
        self.content = content
        self.summary = ""

    def generate_summary(self):
        # Simple summarization logic (for demonstration)
        self.summary = ' '.join(self.content.split()[:50]) + '...'  # First 50 words
        return self.summary

class Ranking:
    def __init__(self, user_preferences):
        self.user_preferences = user_preferences

    def rank_articles(self, articles):
        ranked_articles = sorted(articles, key=lambda x: self._score_article(x), reverse=True)
        return ranked_articles

    def _score_article(self, article):
        score = 0
        for keyword in self.user_preferences.values():
            if keyword in article.content:
                score += 1
        return score

class SearchEngine:
    def __init__(self):
        self.index = None
        self.ranking = None
        self.summary = None

    def search(self, query):
        # Implementation of search functionality
        pass

def load_articles(filename='articles.txt'):
    articles = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                articles.append(Article(line.strip()))
    except FileNotFoundError:
        pass
    return articles