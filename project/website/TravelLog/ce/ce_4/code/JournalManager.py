class JournalManager:
    def __init__(self, entries_file: str):
        self.entries_file = entries_file

    def create_entry(self, destination: str, dates: str, activities: str, reflections: str) -> bool:
        with open(self.entries_file, 'a') as file:
            file.write(f"{destination}|{dates}|{activities}|{reflections}\n")
        return True

    def load_entries(self) -> list:
        entries = []
        try:
            with open(self.entries_file, 'r') as file:
                for line in file:
                    entries.append(line.strip().split('|'))
        except FileNotFoundError:
            open(self.entries_file, 'w').close()  # Create file if it doesn't exist
        return entries

    def edit_entry(self, entry_id: int, updated_data: dict) -> bool:
        entries = self.load_entries()
        if 0 <= entry_id < len(entries):
            entries[entry_id] = [
                updated_data.get('destination', entries[entry_id][0]),
                updated_data.get('dates', entries[entry_id][1]),
                updated_data.get('activities', entries[entry_id][2]),
                updated_data.get('reflections', entries[entry_id][3])
            ]
            self._save_entries(entries)
            return True
        return False

    def delete_entry(self, entry_id: int) -> bool:
        entries = self.load_entries()
        if 0 <= entry_id < len(entries):
            del entries[entry_id]
            self._save_entries(entries)
            return True
        return False

    def search_entries(self, query: str) -> list:
        entries = self.load_entries()
        return [entry for entry in entries if query.lower() in entry[0].lower()]

    def _save_entries(self, entries: list):
        with open(self.entries_file, 'w') as file:
            for entry in entries:
                file.write('|'.join(entry) + '\n')