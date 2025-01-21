class JournalEntry:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.date = self.get_current_date()

    def get_current_date(self) -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save_entry(self) -> None:
        with open('journal_entries.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}|{self.date}\n")

    @staticmethod
    def load_entries() -> list:
        entries = []
        try:
            with open('journal_entries.txt', 'r') as file:
                for line in file:
                    title, content, date = line.strip().split('|')
                    entries.append(JournalEntry(title, content))
                    entries[-1].date = date  # Set the date after creating the entry
        except FileNotFoundError:
            pass
        return entries