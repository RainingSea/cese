from user import User
from journal_entry import JournalEntry
from datetime import datetime

class JournalApp:
    def __init__(self, users_file: str, entries_file: str):
        self.users_file = users_file
        self.entries_file = entries_file

    def register(self, username: str, password: str) -> bool:
        user = User(username, password)
        user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        user = User(username, password)
        return user.validate()

    def create_entry(self, title: str, content: str) -> None:
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = JournalEntry(title, content, date)
        entry.save()

    def get_entries(self) -> list:
        entries = []
        with open(self.entries_file, 'r') as f:
            for line in f:
                title, content, date = line.strip().split('|')
                entries.append({'title': title, 'content': content, 'date': date})
        return entries