import json
import os
from transformers import pipeline

class NewsManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.articles = self.load_articles()
        self.summarizer = pipeline("summarization")

    def load_articles(self) -> list:
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r') as file:
            return [json.loads(line) for line in file.readlines()]

    def save_articles(self) -> None:
        with open(self.file_path, 'w') as file:
            for article in self.articles:
                file.write(f"{json.dumps(article)}\n")

    def generate_summary(self, article: str) -> str:
        summary = self.summarizer(article, max_length=50, min_length=25, do_sample=False)
        return summary[0]['summary_text']

    def rank_articles(self, preferences: dict) -> list:
        ranked_articles = []
        for article in self.articles:
            if any(pref in article['title'].lower() for pref in preferences.get('news', [])):
                ranked_articles.append(article)
        return ranked_articles or self.articles