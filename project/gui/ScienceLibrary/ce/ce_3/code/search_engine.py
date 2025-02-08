import json
from article import Article

class SearchEngine:
    def __init__(self, articles_file: str):
        self.articles = self.load_articles(articles_file)

    def load_articles(self, articles_file: str):
        with open(articles_file, 'r') as file:
            data = json.load(file)
            return [Article(**article) for article in data]

    def search(self, query: str):
        return [article for article in self.articles if query.lower() in article.title.lower() or query.lower() in article.content.lower()]