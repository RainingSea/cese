import json

class JournalEntry:
    def __init__(self, destination: str, dates: str, activities: str, photos: list, reflections: str):
        self.destination = destination
        self.dates = dates
        self.activities = activities
        self.photos = photos
        self.reflections = reflections

    def to_dict(self):
        return {
            'destination': self.destination,
            'dates': self.dates,
            'activities': self.activities,
            'photos': self.photos,
            'reflections': self.reflections
        }

class JournalEntryManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.entries = self.load_entries()

    def load_entries(self) -> list:
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def create_entry(self, destination: str, dates: str, activities: str, photos: list, reflections: str) -> None:
        entry = JournalEntry(destination, dates, activities, photos, reflections)
        self.entries.append(entry.to_dict())
        self.save_entries()

    def update_entry(self, entry_id: int, destination: str, dates: str, activities: str, photos: list, reflections: str) -> None:
        if 0 <= entry_id < len(self.entries):
            self.entries[entry_id] = JournalEntry(destination, dates, activities, photos, reflections).to_dict()
            self.save_entries()

    def delete_entry(self, entry_id: int) -> None:
        if 0 <= entry_id < len(self.entries):
            del self.entries[entry_id]
            self.save_entries()

    def get_entry(self, entry_id: int) -> dict:
        if 0 <= entry_id < len(self.entries):
            return self.entries[entry_id]
        return None

    def search_entries(self, query: str) -> list:
        return [entry for entry in self.entries if query.lower() in entry['destination'].lower()]

    def save_entries(self) -> None:
        with open(self.filename, 'w') as f:
            json.dump(self.entries, f, indent=4)