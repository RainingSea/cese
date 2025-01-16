import json
from user import User

class UserManager:
    def __init__(self):
        self.users_file = 'users.json'
        self.users = self.load_users()

    def load_users(self):
        try:
            with open(self.users_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open(self.users_file, 'w') as file:
            json.dump(self.users, file)

    def register_user(self, username, password):
        if username not in self.users:
            self.users[username] = password
            self.save_users()
            return True
        return False

    def login_user(self, username, password):
        return self.users.get(username) == password

    def user_exists(self, username):
        return username in self.users

    def logout_user(self, username):
        pass  # No action needed for logout in this implementation