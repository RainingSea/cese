import os

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.users = {}

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def get_user_notes(self, username: str) -> list:
        notes_file = f"{username}_notes.txt"
        if os.path.exists(notes_file):
            with open(notes_file, 'r') as file:
                return [line.strip() for line in file]
        return []