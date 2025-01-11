class Article:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "content": self.content
        }