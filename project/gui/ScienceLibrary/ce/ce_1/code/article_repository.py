import json
from typing import List, Dict

class ArticleRepository:
    def __init__(self):
        self.data = self.load_articles()

    def load_articles(self) -> List[Dict]:
        try:
            with open('articles.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_article(self, article: Dict):
        self.data.append(article)
        with open('articles.json', 'w') as file:
            json.dump(self.data, file, indent=4)

    def get_saved_articles(self) -> List[Dict]:
        try:
            with open('saved_articles.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def load_annotations(self) -> Dict:
        try:
            with open('annotations.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_annotation(self, article_id: str, annotation: str):
        annotations = self.load_annotations()
        annotations[article_id] = annotation
        with open('annotations.json', 'w') as file:
            json.dump(annotations, file, indent=4)