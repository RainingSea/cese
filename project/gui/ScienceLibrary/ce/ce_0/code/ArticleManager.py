import json
from typing import List
from Article import Article

class ArticleManager:
    def __init__(self):
        self.articles = []

    def load_articles(self, filename: str) -> None:
        with open(filename, 'r') as file:
            data = json.load(file)
            self.articles = [Article(**article) for article in data]

    def save_favorite(self, article_id: str) -> None:
        favorites = self.get_favorites()
        favorites.append(article_id)
        with open('favorites.json', 'w') as file:
            json.dump(favorites, file)

    def add_annotation(self, article_id: str, annotation: str) -> None:
        annotations = self.get_annotations()
        annotations[article_id] = annotations.get(article_id, []) + [annotation]
        with open('annotations.json', 'w') as file:
            json.dump(annotations, file)

    def get_favorites(self) -> List[str]:
        try:
            with open('favorites.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def get_annotations(self) -> dict:
        try:
            with open('annotations.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}