class Note:
    def __init__(self, note_id: str, content: str):
        self.id = note_id
        self.content = content
        self.tags = []

    def get_id(self) -> str:
        return self.id

    def get_content(self) -> str:
        return self.content

    def add_tag(self, tag):
        self.tags.append(tag)