from JournalEntry import JournalEntry

class JournalManager:
    def __init__(self, entries_file: str = 'journal_entries.txt'):
        self.entries_file = entries_file

    def create_entry(self, title: str, content: str) -> None:
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = JournalEntry(title, content, date)
        entry.save()

    def load_entries(self) -> list:
        entries = []
        try:
            with open(self.entries_file, 'r') as file:
                for line in file:
                    title, content, date = line.strip().split('|')
                    entries.append(JournalEntry(title, content, date))
        except FileNotFoundError:
            pass
        return entries