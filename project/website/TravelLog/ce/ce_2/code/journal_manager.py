import json
import os

class JournalManager:
    def __init__(self, entries_file):
        self.entries_file = entries_file
        self.load_entries()

    def load_entries(self):
        self.entries = []
        if os.path.exists(self.entries_file):
            with open(self.entries_file, 'r') as file:
                for line in file:
                    self.entries.append(json.loads(line.strip()))

    def create_entry(self, destination: str, dates: str, activities: str, photos: str, reflections: str) -> bool:
        entry = {
            'destination': destination,
            'dates': dates,
            'activities': activities,
            'photos': photos,
            'reflections': reflections
        }
        self.entries.append(entry)
        with open(self.entries_file, 'a') as file:
            file.write(json.dumps(entry) + '\n')
        return True

    def view_entries(self) -> list:
        return self.entries

    def edit_entry(self, entry_id: int, updated_entry: dict) -> bool:
        if 0 <= entry_id < len(self.entries):
            self.entries[entry_id] = updated_entry
            self.save_entries()
            return True
        return False

    def delete_entry(self, entry_id: int) -> bool:
        if 0 <= entry_id < len(self.entries):
            del self.entries[entry_id]
            self.save_entries()
            return True
        return False

    def save_entries(self):
        with open(self.entries_file, 'w') as file:
            for entry in self.entries:
                file.write(json.dumps(entry) + '\n')

    def search_entries(self, query: str) -> list:
        return [entry for entry in self.entries if query in entry['destination'] or query in entry['reflections']]