class Article:
    def __init__(self, id: int, title: str, author: str, content: str, category: str, publication_date: str):
        self.id = id
        self.title = title
        self.author = author
        self.content = content
        self.category = category
        self.publication_date = publication_date