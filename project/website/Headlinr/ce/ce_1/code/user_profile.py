class UserProfile:
    def __init__(self):
        self.preferences = {}

    def load_profile(self) -> dict:
        with open('users.txt', 'r') as file:
            for line in file:
                user, preferences = line.strip().split('|')
                self.preferences[user] = preferences
        return self.preferences

    def save_profile(self, preferences: str) -> None:
        with open('users.txt', 'a') as file:
            file.write(f'new_user|{preferences}\n')