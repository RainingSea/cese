class UserPreferences:
    def __init__(self):
        self.preferences = {}

    def load(self) -> dict:
        try:
            with open('user_preferences.txt', 'r') as f:
                for line in f:
                    key, value = line.strip().split('|')
                    self.preferences[key] = value
        except FileNotFoundError:
            self.preferences = {}
        return self.preferences

    def save(self, preferences: dict) -> None:
        with open('user_preferences.txt', 'w') as f:
            for key, value in preferences.items():
                f.write(f"{key}|{value}\n")