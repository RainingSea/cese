import json

class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.users = self.load_users()

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = {'password': password, 'email': email}
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return username in self.users and self.users[username]['password'] == password

    def load_users(self) -> dict:
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_users(self) -> None:
        with open(self.filename, 'w') as file:
            json.dump(self.users, file)