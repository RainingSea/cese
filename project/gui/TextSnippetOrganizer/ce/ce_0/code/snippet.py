class Snippet:
    def __init__(self, content: str, tags: list, description: str):
        self.content = content
        self.tags = tags
        self.description = description

    def to_string(self) -> str:
        tags_string = ','.join(self.tags)
        return f"{self.content}|{tags_string}|{self.description}"