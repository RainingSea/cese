import os

class ArticleManager:
    def __init__(self):
        self.articles = self.load_articles()

    def load_articles(self):
        if not os.path.exists('articles.txt'):
            return []
        with open('articles.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

    def view_articles(self) -> list:
        return self.articles

    def submit_article(self, article: str) -> bool:
        self.articles.append(article)
        with open('articles.txt', 'a') as file:
            file.write(f"{article}\n")
        return True