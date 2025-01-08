class JournalEntry:
    def __init__(self, title: str, content: str, date: str):
        self.title = title
        self.content = content
        self.date = date

    def save(self) -> None:
        with open('journal_entries.txt', 'a') as entry_file:
            entry_file.write(f"{self.title}|{self.content}|{self.date}\n")