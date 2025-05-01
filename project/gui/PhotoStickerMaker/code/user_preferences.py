import os

class UserPreferences:
    def __init__(self, preferences_file='user_preferences.txt'):
        self.preferences_file = preferences_file

    def load_preferences(self):
        if not os.path.exists(self.preferences_file):
            return {}
        with open(self.preferences_file, 'r') as file:
            preferences = {}
            for line in file:
                key, value = line.strip().split('|')
                preferences[key] = value
            return preferences

    def save_preferences(self, preferences):
        with open(self.preferences_file, 'w') as file:
            for key, value in preferences.items():
                file.write(f"{key}|{value}\n")