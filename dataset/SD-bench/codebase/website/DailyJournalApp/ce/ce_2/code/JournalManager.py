class JournalEntry:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.date = self.get_current_date()

    def get_current_date(self) -> str:
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def save(self):
        with open('journal_entries.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}|{self.date}\n")


class JournalManager:
    def __init__(self, entries_file: str):
        self.entries_file = entries_file

    def add_entry(self, title: str, content: str):
        entry = JournalEntry(title, content)
        entry.save()

    def get_entries(self):
        entries = []
        with open(self.entries_file, 'r') as file:
            for line in file:
                title, content, date = line.strip().split('|')
                entries.append({'title': title, 'content': content, 'date': date})
        return entries