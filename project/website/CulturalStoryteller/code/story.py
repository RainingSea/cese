class Story:
    def __init__(self, title: str, content: str, cultural_origin: str):
        self.title = title
        self.content = content
        self.cultural_origin = cultural_origin

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'content': self.content,
            'cultural_origin': self.cultural_origin
        }