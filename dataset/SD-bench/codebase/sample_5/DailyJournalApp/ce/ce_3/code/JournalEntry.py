class JournalEntry:
    def __init__(self, title: str, date: str, content: str):
        self.title = title
        self.date = date
        self.content = content

    def save(self):
        with open('journal_entries.txt', 'a') as file:
            file.write(f"{self.title},{self.date},{self.content}\n")