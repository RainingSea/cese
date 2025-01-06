class JournalEntry:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.date = self.get_current_date()

    def get_current_date(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save(self):
        with open('journal_entries.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.date}\n")

class JournalManager:
    def create_entry(self, title: str, content: str) -> None:
        entry = JournalEntry(title, content)
        entry.save()

    def load_entries(self) -> list:
        entries = []
        with open('journal_entries.txt', 'r') as f:
            entries = [line.strip().split('|') for line in f.readlines()]
        return entries