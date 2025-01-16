from datetime import datetime

class Entry:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content
        self.date = self.get_current_date()

    def get_current_date(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_string(self) -> str:
        return f"{self.title}|{self.content}|{self.date}"