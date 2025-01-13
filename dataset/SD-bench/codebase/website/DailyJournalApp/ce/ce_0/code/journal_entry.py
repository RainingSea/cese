import datetime

class JournalEntry:
    def __init__(self):
        self.entries = self.get_entries()

    def save_entry(self, title: str, content: str) -> None:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('journal_entries.txt', 'a') as file:
            file.write(f"{title}|{content}|{date}\n")

    def get_entries(self) -> list:
        entries = []
        try:
            with open('journal_entries.txt', 'r') as file:
                for line in file:
                    title, content, date = line.strip().split('|')
                    entries.append({'title': title, 'content': content, 'date': date})
        except FileNotFoundError:
            pass
        return entries