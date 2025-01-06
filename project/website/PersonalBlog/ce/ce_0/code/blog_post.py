class BlogPost:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self):
        pass  # Not needed for this implementation

    @staticmethod
    def load(post_id: int):
        pass  # Not needed for this implementation

    @staticmethod
    def delete(post_id: int):
        pass  # Not needed for this implementation