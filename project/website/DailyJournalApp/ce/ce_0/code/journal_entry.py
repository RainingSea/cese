from datetime import datetime

class JournalEntry:
    def __init__(self, title: str, content: str):
        self.title = title
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.content = content

    def save(self) -> None:
        with open('journal_entries.txt', 'a') as f:
            f.write(f"{self.title}|{self.date}|{self.content}\n")