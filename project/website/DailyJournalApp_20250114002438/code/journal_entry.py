class JournalEntry:
    def __init__(self, title: str, content: str, date: str):
        """Initialize a JournalEntry instance."""
        self.title = title
        self.content = content
        self.date = date

    def save(self) -> None:
        """Save the journal entry to the journal_entries.txt file."""
        with open('journal_entries.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}|{self.date}\n")