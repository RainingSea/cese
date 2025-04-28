class JournalManager:
    def __init__(self, entries_file: str):
        self.entries_file = entries_file
        self.load_entries()

    def load_entries(self):
        self.entries = []
        if os.path.exists(self.entries_file):
            with open(self.entries_file, 'r') as file:
                for line in file:
                    title, content, date = line.strip().split('|')
                    self.entries.append({'title': title, 'content': content, 'date': date})

    def create_entry(self, title: str, content: str) -> bool:
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.entries_file, 'a') as file:
            file.write(f"{title}|{content}|{date}\n")
        self.entries.append({'title': title, 'content': content, 'date': date})
        return True

    def get_entries(self) -> list:
        return self.entries