class BlogPost:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def to_string(self) -> str:
        return f"{self.title}|{self.content}|{self.author}"