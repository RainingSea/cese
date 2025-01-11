from user import User
from journal_entry import JournalEntry

class JournalApp:
    def __init__(self):
        self.users = self.load_users()
        self.entries = self.load_entries()

    def load_users(self):
        users = []
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users.append(User(username, password))
        return users

    def load_entries(self):
        entries = []
        with open('journal_entries.txt', 'r') as f:
            for line in f:
                title, date, content = line.strip().split('|')
                entries.append(JournalEntry(title, content))
                entries[-1].date = date  # Set the loaded date
        return entries

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        return User.validate(username, password)

    def create_entry(self, title: str, content: str) -> None:
        new_entry = JournalEntry(title, content)
        new_entry.save()
        self.entries.append(new_entry)

    def get_entries(self):
        return self.entries