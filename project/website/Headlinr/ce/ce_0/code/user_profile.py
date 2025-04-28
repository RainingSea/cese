class UserProfile:
    def __init__(self):
        self.preferences = self.load_preferences()

    def update_preferences(self, new_preferences: list) -> None:
        self.preferences = new_preferences
        self.save_preferences()

    def get_preferences(self) -> list:
        return self.preferences

    def load_preferences(self) -> list:
        try:
            with open('users.txt', 'r') as file:
                return file.readline().strip().split('|')[1:]  # Assuming the first line contains the preferences
        except FileNotFoundError:
            return []

    def save_preferences(self) -> None:
        with open('users.txt', 'w') as file:
            file.write(f'admin|{"|".join(self.preferences)}\n')  # Saving with a placeholder username