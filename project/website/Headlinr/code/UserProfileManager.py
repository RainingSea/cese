import json
import os

class UserProfileManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.users = self.load_users()

    def load_users(self) -> dict:
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, 'r') as file:
            return {line.split('|')[0]: json.loads(line.split('|')[1]) for line in file.readlines()}

    def save_users(self) -> None:
        with open(self.file_path, 'w') as file:
            for username, preferences in self.users.items():
                file.write(f"{username}|{json.dumps(preferences)}\n")

    def create_user(self, username: str, preferences: dict) -> None:
        if username not in self.users:
            self.users[username] = preferences
            self.save_users()

    def update_preferences(self, username: str, preferences: dict) -> None:
        if username in self.users:
            self.users[username]['preferences'] = preferences
            self.save_users()

    def get_user_preferences(self) -> dict:
        if self.users:
            return self.users[next(iter(self.users))]['preferences']
        return {}