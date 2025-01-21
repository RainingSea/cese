import json

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self) -> dict:
        try:
            with open('users.txt', 'r') as file:
                users = {}
                for line in file:
                    username, preferences = line.strip().split('|')
                    users[username] = json.loads(preferences)
                return users
        except FileNotFoundError:
            return {}

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for username, preferences in self.users.items():
                file.write(f"{username}|{json.dumps(preferences)}\n")

    def add_user(self, username: str, preferences: dict) -> None:
        self.users[username] = preferences
        self.save_users()

    def get_user(self, username: str) -> dict:
        return self.users.get(username, {})