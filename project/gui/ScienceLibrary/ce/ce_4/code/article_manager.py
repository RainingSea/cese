import json

class ArticleManager:
    def __init__(self):
        self.articles = []
        self.favorites = []
        self.annotations = {}

    def load_articles(self):
        with open('articles.json', 'r') as file:
            self.articles = json.load(file)

    def save_favorites(self, article_id):
        if article_id not in self.favorites:
            self.favorites.append(article_id)
            with open('favorites.json', 'w') as file:
                json.dump(self.favorites, file)

    def create_annotation(self, article_id, note):
        if article_id not in self.annotations:
            self.annotations[article_id] = []
        self.annotations[article_id].append(note)
        with open('annotations.json', 'w') as file:
            json.dump(self.annotations, file)