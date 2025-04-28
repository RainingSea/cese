import os
from datetime import datetime

class Main:
    def __init__(self):
        self.user_manager = UserManager('users.txt')
        self.journal_manager = JournalManager('journal_entries.txt')

    def main(self):
        # Placeholder for application flow
        print("Welcome to the Daily Journal App")
        # Here you would typically handle routing to different pages (login, register, etc.)

class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False  # User already exists
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users[username] = password
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class JournalManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_entries()

    def load_entries(self):
        self.entries = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    title, date, content = line.strip().split('|')
                    self.entries.append({'title': title, 'date': date, 'content': content})

    def add_entry(self, title: str, content: str) -> bool:
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f"{title}|{date}|{content}\n"
        with open(self.filename, 'a') as file:
            file.write(entry)
        self.entries.append({'title': title, 'date': date, 'content': content})
        return True

    def get_entries(self) -> list:
        return self.entries

if __name__ == "__main__":
    app = Main()
    app.main()