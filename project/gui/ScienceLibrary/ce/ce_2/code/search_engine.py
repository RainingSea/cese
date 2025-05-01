import json

class SearchEngine:
    def __init__(self):
        self.articles = self.load_articles()

    def load_articles(self):
        with open('articles.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

    def search(self, query: str):
        return [article for article in self.articles if query.lower() in article.lower()]