from datetime import datetime

class JournalEntry:
    def __init__(self, title: str, content: str, date: str = None):
        self.title = title
        self.content = content
        self.date = date if date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save_entry(self):
        pass  # Saving is handled in main.py

    @staticmethod
    def load_entries() -> list:
        return []  # Loading is handled in main.py