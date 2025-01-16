import json

class UserManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.users = self.load_users()

    def load_users(self) -> list:
        try:
            with open(self.file_path, 'r') as file:
                return [line.strip().split('|') for line in file.readlines()]
        except FileNotFoundError:
            return []

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append([username, password])
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)

    def save_users(self):
        with open(self.file_path, 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')

    def get_users(self) -> list:
        return self.users