class Article:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def to_string(self) -> str:
        return f"{self.title}|{self.content}"