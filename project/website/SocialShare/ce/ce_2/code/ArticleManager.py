import json

class Article:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'content': self.content,
            'author': self.author
        }

class ArticleManager:
    def __init__(self):
        self.articles = []

    def load_articles(self) -> None:
        try:
            with open('articles.txt', 'r') as f:
                for line in f:
                    title, content, author = line.strip().split('|')
                    article = Article(title, content, author)
                    self.articles.append(article)
        except FileNotFoundError:
            pass

    def save_article(self, article: Article) -> None:
        self.articles.append(article)
        with open('articles.txt', 'a') as f:
            f.write(f"{article.title}|{article.content}|{article.author}\n")