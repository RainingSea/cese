from knowledge_base import KnowledgeBase

class Index:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.index = {}

    def create_index(self, data):
        for article in data:
            self.index[article['id']] = article

    def query_index(self, query):
        results = []
        for article_id, article in self.index.items():
            if query.lower() in article['title'].lower() or query.lower() in article['content'].lower():
                results.append(article)
        return results