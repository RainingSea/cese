class Resource:
    def __init__(self, title: str, url: str):
        self._title = title
        self._url = url

    def to_string(self) -> str:
        return f"{self._title}|{self._url}"