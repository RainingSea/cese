import json
from nltk import sent_tokenize
import requests

class SearchEngine:
    def __init__(self):
        self.index = {}
        self.ranking = Ranking()
        self.summary = Summary()

    def search(self, query: str) -> str:
        # Simulated search result
        return f"Results for {query}"

class Ranking:
    def rank_articles(self, articles, preferences):
        # Simulated ranking logic
        return sorted(articles, key=lambda x: x['relevance'], reverse=True)

class Summary:
    def generate_summary(self, article: str) -> str:
        sentences = sent_tokenize(article)
        return ' '.join(sentences[:2])  # Return first two sentences as summary

class UserProfile:
    def __init__(self):
        self.preferences = {}

    def set_preferences(self, topics: list, sources: list):
        self.preferences = {'topics': topics, 'sources': sources}

    def get_preferences(self) -> dict:
        return self.preferences

class Bookmark:
    def __init__(self):
        self.bookmarked_articles = []

    def add_bookmark(self, article_id: str):
        self.bookmarked_articles.append(article_id)

    def remove_bookmark(self, article_id: str):
        self.bookmarked_articles.remove(article_id)

    def get_bookmarks(self) -> list:
        return self.bookmarked_articles

class Feedback:
    def __init__(self):
        self.user_feedback = []

    def submit_feedback(self, feedback: str):
        self.user_feedback.append(feedback)

    def get_feedback(self) -> list:
        return self.user_feedback