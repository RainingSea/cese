from entry import Entry

class JournalManager:
    def __init__(self, journal_file: str) -> None:
        self.journal_file = journal_file
        self.entries = []
        self.load_entries()

    def load_entries(self) -> None:
        try:
            with open(self.journal_file, 'r') as file:
                for line in file:
                    title, content, date = line.strip().split('|')
                    entry = Entry(title, content)
                    entry.date = date  # Set the date from the file
                    self.entries.append(entry)
        except FileNotFoundError:
            pass

    def create_entry(self, title: str, content: str) -> None:
        entry = Entry(title, content)
        self.entries.append(entry)
        with open(self.journal_file, 'a') as file:
            file.write(entry.to_string() + "\n")

    def get_entries(self) -> list:
        return self.entries