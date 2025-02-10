class Story:
    def __init__(self, title: str, content: str, cultural_origin: str, category: str):
        self.title = title
        self.content = content
        self.cultural_origin = cultural_origin
        self.category = category

    def save(self):
        pass  # Not needed for this implementation

    def load(self):
        return {
            "title": self.title,
            "content": self.content,
            "cultural_origin": self.cultural_origin,
            "category": self.category
        }