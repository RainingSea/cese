import json
from article import Article

class ArticleManager:
    def __init__(self, saved_articles_file: str, annotations_file: str):
        self.saved_articles = self.load_saved_articles(saved_articles_file)
        self.annotations = self.load_annotations(annotations_file)

    def load_saved_articles(self, saved_articles_file: str):
        with open(saved_articles_file, 'r') as file:
            data = json.load(file)
            return [Article(**article) for article in data]

    def load_annotations(self, annotations_file: str):
        with open(annotations_file, 'r') as file:
            return json.load(file)

    def save_article(self, article: Article):
        self.saved_articles.append(article)
        self.save_to_file('saved_articles.json', self.saved_articles)

    def organize_articles(self, category: str):
        return [article for article in self.saved_articles if article.category == category]

    def add_annotation(self, article_id: int, note: str):
        if article_id not in self.annotations:
            self.annotations[article_id] = []
        self.annotations[article_id].append(note)
        self.save_to_file('annotations.json', self.annotations)

    def save_to_file(self, filename: str, data):
        with open(filename, 'w') as file:
            json.dump([article.__dict__ for article in data], file)