class JournalManager:
    def __init__(self, entries_file: str):
        self.entries_file = entries_file
        self.entries = self.load_entries()

    def create_entry(self, title: str, content: str) -> None:
        entry = f"{title}|{content}\n"
        with open(self.entries_file, 'a') as file:
            file.write(entry)
        self.entries.append({'title': title, 'content': content})

    def load_entries(self) -> list:
        entries = []
        try:
            with open(self.entries_file, 'r') as file:
                for line in file:
                    title, content = line.strip().split('|')
                    entries.append({'title': title, 'content': content})
        except FileNotFoundError:
            pass
        return entries