from datetime import datetime

class JournalEntry:
    def __init__(self, title: str, date: str, content: str):
        self.title = title
        self.date = date
        self.content = content

    def save(self) -> None:
        with open('journal_entries.txt', 'a') as f:
            f.write(f"{self.title}|{self.date}|{self.content}\n")


class JournalManager:
    def __init__(self):
        self.entries = []

    def create_entry(self, title: str, content: str) -> None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = JournalEntry(title, date, content)
        new_entry.save()
        self.entries.append(new_entry)

    def load_entries(self) -> None:
        try:
            with open('journal_entries.txt', 'r') as f:
                for line in f:
                    title, date, content = line.strip().split('|')
                    self.entries.append(JournalEntry(title, date, content))
        except FileNotFoundError:
            pass

    def get_entries(self):
        return self.entries

    def cleanup_entries(self) -> None:
        open('journal_entries.txt', 'w').close()  # Clear the journal entries file