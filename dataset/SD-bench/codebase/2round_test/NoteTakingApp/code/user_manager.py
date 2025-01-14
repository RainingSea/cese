import os

class UserManager:
    def __init__(self, users_file):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()  # Create file if it doesn't exist
        with open(self.users_file, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')[:2]
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

    def get_users(self) -> list:
        return list(self.users.keys())