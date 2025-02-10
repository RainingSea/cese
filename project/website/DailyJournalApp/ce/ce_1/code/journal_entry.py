import json
from datetime import datetime

class JournalEntry:
    def __init__(self, title: str = '', content: str = ''):
        self.title = title
        self.content = content
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save(self) -> None:
        entry_data = {'title': self.title, 'content': self.content, 'date': self.date}
        with open('entries.txt', 'a') as file:
            file.write(json.dumps(entry_data) + '\n')

    def load_all(self) -> list:
        entries = []
        try:
            with open('entries.txt', 'r') as file:
                entries = [json.loads(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            pass
        return entries