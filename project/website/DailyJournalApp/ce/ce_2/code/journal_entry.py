class JournalEntry:
    def __init__(self, title: str, date: str, content: str):
        self.title = title
        self.date = date
        self.content = content

    def save(self) -> None:
        with open('journal_entries.txt', 'a') as file:
            file.write(f"{self.title}|{self.date}|{self.content}\n")

    def get_entries(self) -> list:
        entries = []
        with open('journal_entries.txt', 'r') as file:
            for line in file:
                title, date, content = line.strip().split('|')
                entries.append(JournalEntry(title, date, content))
        return entries