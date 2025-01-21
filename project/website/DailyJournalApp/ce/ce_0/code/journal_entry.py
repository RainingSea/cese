import datetime

class JournalEntry:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save(self) -> None:
        with open('journal_entries.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.date}\n")

    def load_entries(self) -> list:
        entries = []
        try:
            with open('journal_entries.txt', 'r') as f:
                for line in f:
                    title, content, date = line.strip().split('|')
                    entries.append({'title': title, 'content': content, 'date': date})
        except FileNotFoundError:
            pass  # File does not exist yet
        return entries