import os
import json

class PreferenceManager:
    def __init__(self):
        self.preferences = {}

    def save_preferences(self, username: str, preferences: dict) -> None:
        self.preferences[username] = preferences
        self.save_all_preferences()

    def load_preferences(self, username: str) -> dict:
        return self.preferences.get(username, {})

    def load_all_preferences(self) -> None:
        if os.path.exists('preferences.txt'):
            with open('preferences.txt', 'r') as file:
                for line in file:
                    username, preferences = line.strip().split('|')
                    self.preferences[username] = json.loads(preferences)

    def save_all_preferences(self) -> None:
        with open('preferences.txt', 'w') as file:
            for username, preferences in self.preferences.items():
                file.write(f"{username}|{json.dumps(preferences)}\n")