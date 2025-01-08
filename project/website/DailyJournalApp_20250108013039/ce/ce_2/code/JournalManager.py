from JournalEntry import JournalEntry

class JournalManager:
    def __init__(self, entries_file: str):
        self.entries_file = entries_file

    def add_entry(self, entry: JournalEntry) -> None:
        entry.save()

    def get_all_entries(self) -> list:
        entries = []
        with open(self.entries_file, 'r') as file:
            for line in file:
                title, content, date = line.strip().split('|')
                entries.append(JournalEntry(title, content, date))
        return entries