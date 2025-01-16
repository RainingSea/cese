import json
from typing import List

class Article:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "content": self.content,
            "author": self.author
        }

class ArticleManager:
    def __init__(self, articles_file: str):
        self.articles_file = articles_file
        self.articles: List[Article] = []
        self.load_articles()

    def load_articles(self) -> None:
        try:
            with open(self.articles_file, 'r') as f:
                articles_data = json.load(f)
                self.articles = [Article(**article) for article in articles_data]
        except FileNotFoundError:
            self.articles = []

    def save_articles(self) -> None:
        with open(self.articles_file, 'w') as f:
            json.dump([article.to_dict() for article in self.articles], f)

    def add_article(self, title: str, content: str, author: str) -> None:
        new_article = Article(title, content, author)
        self.articles.append(new_article)
        self.save_articles()

    def get_articles(self) -> List[Article]:
        return self.articles

    def update_article(self, title: str, new_content: str) -> None:
        for article in self.articles:
            if article.title == title:
                article.content = new_content
                self.save_articles()
                return
        raise ValueError("Article not found.")

    def get_article_comments(self, article_id: str) -> List[str]:
        # Placeholder for fetching comments related to an article
        return []