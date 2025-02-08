from typing import List
from KnowledgeBase import KnowledgeBase

class Index:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.index = {}

    def create_index(self, data: List[dict]) -> None:
        for article in data:
            self.index[article['id']] = article

    def query_index(self, query: str) -> List[dict]:
        results = []
        for article in self.index.values():
            if query.lower() in article['title'].lower() or query.lower() in article['content'].lower():
                results.append(article)
        return results