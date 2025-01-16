class JournalEntry:
    def __init__(self, title: str = '', content: str = '', date: str = ''):
        self.title = title
        self.content = content
        self.date = date

    def save_entry(self) -> None:
        with open('journal_entries.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.date}\n")

    def load_entries(self) -> list:
        entries = []
        try:
            with open('journal_entries.txt', 'r') as f:
                for line in f:
                    title, content, date = line.strip().split('|')
                    entries.append(JournalEntry(title, content, date))
        except FileNotFoundError:
            pass
        return entries