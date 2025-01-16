from datetime import datetime

class JournalEntry:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_string(self) -> str:
        return f"{self.title}|{self.content}|{self.date}"