from JournalEntry import JournalEntry

class JournalManager:
    def __init__(self):
        self.entries = self.load_entries()

    def load_entries(self) -> list:
        entries = []
        try:
            with open('entries.txt', 'r') as file:
                for line in file:
                    username, destination, dates, activities, photos_str, reflections = line.strip().split('|')
                    photos = photos_str.split(',') if photos_str else []
                    entries.append(JournalEntry(username, destination, dates, activities, photos, reflections))
        except FileNotFoundError:
            pass
        return entries

    def add_entry(self, entry: JournalEntry) -> None:
        self.entries.append(entry)
        entry.save()

    def delete_entry(self, entry_id: int) -> None:
        # Placeholder for delete functionality
        pass

    def edit_entry(self, entry_id: int, new_entry: JournalEntry) -> None:
        # Placeholder for edit functionality
        pass