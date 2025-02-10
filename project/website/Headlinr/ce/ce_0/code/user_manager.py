import json

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def load_users(self):
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, preferences = line.strip().split('|')
                    self.users[username] = json.loads(preferences)
        except FileNotFoundError:
            pass

    def save_users(self):
        with open('users.txt', 'w') as file:
            for username, preferences in self.users.items():
                file.write(f"{username}|{json.dumps(preferences)}\n")

    def create_user(self, username: str, preferences: list):
        if username not in self.users:
            self.users[username] = preferences
            self.save_users()

    def update_preferences(self, username: str, preferences: list):
        if username in self.users:
            self.users[username] = preferences
            self.save_users()

    def get_user_preferences(self):
        # For simplicity, return preferences of the first user
        return list(self.users.values())[0] if self.users else []

    def get_bookmarked_articles(self):
        # Placeholder for retrieving bookmarked articles
        return []