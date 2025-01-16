import json
import os

class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename, 'r') as file:
            return json.load(file)

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def get_users(self) -> list:
        return list(self.users.keys())

    def delete_user(self, username: str) -> bool:
        if username in self.users:
            del self.users[username]
            self.save_users()
            return True
        return False

    def save_users(self):
        with open(self.filename, 'w') as file:
            json.dump(self.users, file)