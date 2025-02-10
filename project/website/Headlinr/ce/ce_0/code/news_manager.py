import json

class NewsManager:
    def __init__(self):
        self.articles = []
        self.preferences = {}

    def load_articles(self):
        try:
            with open('articles.txt', 'r') as file:
                for line in file:
                    self.articles.append(line.strip())
        except FileNotFoundError:
            pass

    def summarize_article(self, article: str) -> str:
        # Simple summarization by returning the first 50 characters
        return article[:50] + '...' if len(article) > 50 else article

    def rank_articles(self, preferences: list) -> list:
        # For simplicity, return articles as is
        return self.articles

    def bookmark_article(self, username: str, article_id: int):
        # Placeholder for bookmarking logic
        pass