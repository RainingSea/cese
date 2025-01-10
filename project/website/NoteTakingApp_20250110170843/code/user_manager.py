import json
import bcrypt
import os

class UserManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.load_users()

    def load_users(self):
        """Loads users from the JSON file."""
        self.users = {}
        if not os.path.exists(self.file_path):
            return
        with open(self.file_path, 'r') as file:
            users_data = json.load(file)
            for user in users_data:
                self.users[user['username']] = user['hashed_password']

    def register(self, username: str, password: str) -> bool:
        """Registers a new user."""
        if username in self.users:
            return False
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with open(self.file_path, 'a') as file:
            json.dump({"username": username, "hashed_password": hashed_password.decode('utf-8')}, file)
            file.write('\n')
        self.users[username] = hashed_password.decode('utf-8')
        return True

    def login(self, username: str, password: str) -> bool:
        """Validates user login credentials."""
        if username not in self.users:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.users[username].encode('utf-8'))

    def get_users(self) -> list:
        """Returns a list of registered usernames."""
        return list(self.users.keys())