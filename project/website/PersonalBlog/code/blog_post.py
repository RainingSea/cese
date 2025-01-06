class BlogPost:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self):
        pass  # Not needed for file-based storage

    @classmethod
    def load(cls, post_id: int):
        pass  # Not needed for file-based storage

    @classmethod
    def delete(cls, post_id: int):
        pass  # Not needed for file-based storage