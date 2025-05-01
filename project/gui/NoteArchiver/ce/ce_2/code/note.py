class Note:
    def __init__(self, content: str):
        self.content = content
        self.tags = []

    def add_tag(self, tag: str) -> None:
        self.tags.append(tag)