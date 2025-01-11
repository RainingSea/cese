class JournalEntry:
    def __init__(self, title: str, content: str, date: str):
        self.title = title
        self.content = content
        self.date = date

    def save_entry(self) -> None:
        with open('journal_entries.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}|{self.date}\n")

    @staticmethod
    def load_entries() -> list:
        entries = []
        with open('journal_entries.txt', 'r') as file:
            for line in file:
                title, content, date = line.strip().split('|')
                entries.append(JournalEntry(title, content, date))
        return entries