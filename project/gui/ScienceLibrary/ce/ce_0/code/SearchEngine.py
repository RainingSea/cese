from Index import Index

class SearchEngine:
    def __init__(self):
        self.index = Index()
        self.index.create_index(self.index.knowledge_base.fetch_data())

    def search(self, query: str) -> list:
        return self.index.query_index(query)