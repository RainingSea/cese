import os

class ArticleManager:
    def __init__(self):
        self.articles = self.load_articles()
        self.favorites = self.get_favorites()
        self.annotations = self.load_annotations()

    def load_articles(self):
        if not os.path.exists('articles.txt'):
            return []
        with open('articles.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

    def save_favorite(self, article_id: str):
        with open('favorites.txt', 'a') as file:
            file.write(f"{article_id}\n")

    def add_annotation(self, article_id: str, annotation: str):
        self.annotations[article_id] = annotation
        self.save_annotations()

    def get_favorites(self):
        if not os.path.exists('favorites.txt'):
            return []
        with open('favorites.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

    def load_annotations(self):
        if not os.path.exists('annotations.txt'):
            return {}
        with open('annotations.txt', 'r') as file:
            annotations = {}
            for line in file:
                article_id, annotation = line.strip().split('|')
                annotations[article_id] = annotation
            return annotations

    def save_annotations(self):
        with open('annotations.txt', 'w') as file:
            for article_id, annotation in self.annotations.items():
                file.write(f"{article_id}|{annotation}\n")