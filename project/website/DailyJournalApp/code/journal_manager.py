from datetime import datetime

class JournalEntry:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save(self):
        with open('journal_entries.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}|{self.date}\n")

class JournalManager:
    def create_entry(self, title: str, content: str):
        entry = JournalEntry(title, content)
        entry.save()

    def load_entries(self) -> list:
        entries = []
        with open('journal_entries.txt', 'r') as file:
            for line in file:
                title, content, date = line.strip().split('|')
                entries.append({'title': title, 'content': content, 'date': date})
        return entries