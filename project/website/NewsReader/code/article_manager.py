import os
from typing import List

class ArticleManager:
    def __init__(self):
        self.articles: List[List[str]] = []
        self.load_articles()

    def load_articles(self) -> None:
        if os.path.exists('articles.txt'):
            with open('articles.txt', 'r') as file:
                self.articles = [line.strip().split('|') for line in file.readlines()]

    def get_articles_by_category(self, category: str) -> List[List[str]]:
        return [article for article in self.articles if article[1] == category]

    def search_articles(self, query: str) -> List[List[str]]:
        return [article for article in self.articles if query.lower() in article[0].lower()]

    def get_article_details(self, article_id: int) -> List[str]:
        if 0 <= article_id < len(self.articles):
            return self.articles[article_id]
        return ["Article not found."]