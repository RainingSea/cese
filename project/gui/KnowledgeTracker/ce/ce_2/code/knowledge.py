class Knowledge:
    def __init__(self, title: str, category: str, content: str):
        self.title = title
        self.category = category
        self.content = content

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "category": self.category,
            "content": self.content
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Knowledge':
        return cls(
            title=data.get("title", ""),
            category=data.get("category", ""),
            content=data.get("content", "")
        )