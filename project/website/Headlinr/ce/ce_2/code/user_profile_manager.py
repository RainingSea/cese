import json

class UserProfileManager:
    def __init__(self):
        self.user_profiles = self.load_profiles()

    def load_profiles(self) -> dict:
        try:
            with open('users.txt', 'r') as file:
                profiles = {}
                for line in file:
                    user_id, preferences = line.strip().split('|')
                    profiles[user_id] = preferences.split(',')
                return profiles
        except FileNotFoundError:
            return {}

    def save_profiles(self) -> None:
        with open('users.txt', 'w') as file:
            for user_id, preferences in self.user_profiles.items():
                file.write(f"{user_id}|{','.join(preferences)}\n")

    def add_user(self, user_data: dict) -> None:
        self.user_profiles[user_data['user_id']] = user_data['preferences']
        self.save_profiles()

    def update_preferences(self, user_id: str, preferences: list) -> None:
        if user_id in self.user_profiles:
            self.user_profiles[user_id] = preferences
            self.save_profiles()