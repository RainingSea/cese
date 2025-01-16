from user import User
from journal_entry import JournalEntry

class TravelLogApp:
    def __init__(self):
        self.users = User.load_all()
        self.entries = JournalEntry.load_all()

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user.username == username and user.password == password for user in self.users)

    def create_entry(self, destination: str, date: str, activities: str, photos: list, reflections: str):
        new_entry = JournalEntry(destination, date, activities, photos, reflections)
        new_entry.save()
        self.entries.append(new_entry)

    def view_entries(self) -> list:
        return self.entries

    def search_entries(self, query: str) -> list:
        return [entry for entry in self.entries if query in entry.destination or query in entry.date]

    def share_entry(self, entry_id: int) -> str:
        # This method will be implemented in the future
        return f"Shareable link for entry {entry_id}"