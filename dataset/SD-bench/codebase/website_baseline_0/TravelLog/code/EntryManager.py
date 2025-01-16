from models import JournalEntry
import ast

class EntryManager:
    def __init__(self, entries_file: str = 'entries.txt'):
        self.entries_file = entries_file

    def load_entries(self):
        entries = []
        try:
            with open(self.entries_file, 'r') as file:
                for line in file:
                    entry_data = ast.literal_eval(line.strip())
                    entry = JournalEntry(
                        entry_data['destination'],
                        entry_data['dates'],
                        entry_data['activities'],
                        entry_data['photos'],
                        entry_data['reflections']
                    )
                    entries.append(entry)
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return entries

    def save_entry(self, entry: JournalEntry):
        entry.save()

    def find_entries_by_destination(self, destination: str):
        entries = self.load_entries()
        return [entry for entry in entries if entry.destination == destination]

    def edit_entry(self, old_entry: JournalEntry, new_entry: JournalEntry):
        entries = self.load_entries()
        for index, entry in enumerate(entries):
            if entry.destination == old_entry.destination and entry.dates == old_entry.dates:
                entries[index] = new_entry
                self._save_all_entries(entries)
                return True
        return False

    def delete_entry(self, entry: JournalEntry):
        entries = self.load_entries()
        entries = [e for e in entries if not (e.destination == entry.destination and e.dates == entry.dates)]
        self._save_all_entries(entries)

    def _save_all_entries(self, entries):
        with open(self.entries_file, 'w') as file:
            for entry in entries:
                file.write(f"{entry.to_dict()}\n")

    def search_entries(self, search_term: str):
        entries = self.load_entries()
        return [entry for entry in entries if search_term.lower() in entry.destination.lower() or search_term.lower() in entry.activities.lower() or search_term.lower() in entry.reflections.lower()]

    def share_entry(self, entry: JournalEntry):
        # Placeholder for sharing functionality
        return f"Entry shared: {entry.to_dict()}"