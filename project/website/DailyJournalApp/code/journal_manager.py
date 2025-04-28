from datetime import datetime

class JournalManager:
    def __init__(self, entries_file: str):
        self.entries_file = entries_file
        self.load_entries()

    def load_entries(self):
        self.entries = []
        try:
            with open(self.entries_file, 'r') as file:
                for line in file:
                    username, title, content, date = line.strip().split('|')
                    self.entries.append({
                        'username': username,
                        'title': title,
                        'content': content,
                        'date': date
                    })
        except FileNotFoundError:
            open(self.entries_file, 'w').close()  # Create the file if it doesn't exist

    def create_entry(self, username: str, title: str, content: str) -> bool:
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f"{username}|{title}|{content}|{date}\n"
        with open(self.entries_file, 'a') as file:
            file.write(entry)
        self.entries.append({'username': username, 'title': title, 'content': content, 'date': date})
        return True

    def get_entries(self, username: str) -> list:
        return [entry for entry in self.entries if entry['username'] == username]

    def delete_entry(self, entry_id: int) -> bool:
        if 0 <= entry_id < len(self.entries):
            del self.entries[entry_id]
            self.save_entries()
            return True
        return False

    def save_entries(self):
        with open(self.entries_file, 'w') as file:
            for entry in self.entries:
                file.write(f"{entry['username']}|{entry['title']}|{entry['content']}|{entry['date']}\n")