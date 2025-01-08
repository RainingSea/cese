from JournalEntry import JournalEntry

class JournalManager:
    def __init__(self, entries_file: str):
        self.entries_file = entries_file
        self.load_entries()

    def load_entries(self) -> None:
        self.entries = []
        try:
            with open(self.entries_file, 'r') as file:
                for line in file:
                    title, content, date = line.strip().split('|')
                    self.entries.append(JournalEntry(title, content, date))
        except FileNotFoundError:
            pass

    def add_entry(self, entry: JournalEntry) -> None:
        entry.save()
        self.entries.append(entry)

    def get_all_entries(self) -> list:
        return self.entries