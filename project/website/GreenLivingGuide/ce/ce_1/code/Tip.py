class Tip:
    def __init__(self, content: str):
        self.content = content

    def to_string(self) -> str:
        return self.content