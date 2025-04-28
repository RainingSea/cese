import os

class EntryManager:
    def __init__(self):
        self.entries = []

    def create_entry(self, destination: str, dates: str, activities: str, photos: str, reflections: str) -> None:
        entry_id = len(self.entries) + 1
        entry = {
            'id': entry_id,
            'destination': destination,
            'dates': dates,
            'activities': activities,
            'photos': photos,
            'reflections': reflections
        }
        self.entries.append(entry)
        self.save_entries()

    def edit_entry(self, entry_id: int, updated_entry: dict) -> None:
        for entry in self.entries:
            if entry['id'] == entry_id:
                entry.update(updated_entry)
                self.save_entries()
                break

    def delete_entry(self, entry_id: int) -> None:
        self.entries = [entry for entry in self.entries if entry['id'] != entry_id]
        self.save_entries()

    def load_entries(self) -> None:
        if os.path.exists('entries.txt'):
            with open('entries.txt', 'r') as file:
                for line in file:
                    entry_data = line.strip().split('|')
                    entry = {
                        'id': int(entry_data[0]),
                        'destination': entry_data[1],
                        'dates': entry_data[2],
                        'activities': entry_data[3],
                        'photos': entry_data[4],
                        'reflections': entry_data[5]
                    }
                    self.entries.append(entry)

    def save_entries(self) -> None:
        with open('entries.txt', 'w') as file:
            for entry in self.entries:
                file.write(f"{entry['id']}|{entry['destination']}|{entry['dates']}|{entry['activities']}|{entry['photos']}|{entry['reflections']}\n")