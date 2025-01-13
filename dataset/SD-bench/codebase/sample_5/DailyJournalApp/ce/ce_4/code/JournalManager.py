class JournalEntry:
    def __init__(self, title: str, date: str, content: str) -> None:
        self.title = title
        self.date = date
        self.content = content

    def save(self) -> None:
        with open('journal_entries.txt', 'a') as file:
            file.write(f"{self.title},{self.date},{self.content}\n")


class JournalManager:
    def __init__(self):
        self.entries = []
        self.load_entries()

    def create_entry(self, title: str, content: str) -> None:
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = JournalEntry(title, date, content)
        entry.save()
        self.entries.append(entry)

    def load_entries(self) -> None:
        try:
            with open('journal_entries.txt', 'r') as file:
                for line in file:
                    title, date, content = line.strip().split(',', 2)
                    self.entries.append(JournalEntry(title, date, content))
        except FileNotFoundError:
            pass