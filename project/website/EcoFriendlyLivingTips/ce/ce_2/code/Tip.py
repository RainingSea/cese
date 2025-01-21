class Tip:
    def __init__(self, title: str, content: str, author: str):
        self._title = title
        self._content = content
        self._author = author

    def to_string(self) -> str:
        return f"{self._title}|{self._content}|{self._author}"