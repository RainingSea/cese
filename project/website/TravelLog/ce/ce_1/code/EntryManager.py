class EntryManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.entries = self.load_entries()

    def create_entry(self, username: str, destination: str, date: str, activities: str, photos: str, reflections: str) -> None:
        entry = f"{username},{destination},{date},{activities},{photos},{reflections}\n"
        with open(self.filename, 'a') as f:
            f.write(entry)
        self.entries.append(entry.strip())

    def load_entries(self) -> list:
        try:
            with open(self.filename, 'r') as f:
                return f.read().strip().split('\n')
        except FileNotFoundError:
            return []

    def edit_entry(self, entry_id: int, new_data: dict) -> None:
        # Implementation to edit an entry (not required in this task)
        pass

    def delete_entry(self, entry_id: int) -> None:
        # Implementation to delete an entry (not required in this task)
        pass

    def search_entries(self, query: str) -> list:
        # Implementation to search for entries (not required in this task)
        pass