from datetime import datetime

class JournalEntry:
    def __init__(self, title: str, content: str, date: str = None):
        self.title = title
        self.content = content
        self.date = date if date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save(self):
        # This method is not needed as we are saving entries directly in the main.py
        pass

    def load_entries(self):
        # This method is not needed as we are loading entries directly in the main.py
        pass