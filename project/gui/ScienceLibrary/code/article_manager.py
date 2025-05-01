import json

class Article:
    def __init__(self, title: str, author: str, description: str):
        self.title = title
        self.author = author
        self.description = description

    def __str__(self):
        return f"{self.title} by {self.author}: {self.description}"

class ArticleManager:
    def __init__(self):
        self.articles = []

    def load_articles(self):
        try:
            with open('articles.json', 'r') as file:
                articles_data = json.load(file)
                self.articles = [Article(**data) for data in articles_data]
        except FileNotFoundError:
            self.articles = []

    def search(self, query: str):
        query = query.lower()
        return [article.title for article in self.articles if query in article.title.lower() or query in article.description.lower()]

    def get_article(self, title: str):
        for article in self.articles:
            if article.title == title:
                return article
        return None

    def add_annotation(self, title: str, note: str):
        # This method is added to allow annotations to be added directly from the ArticleManager
        pass