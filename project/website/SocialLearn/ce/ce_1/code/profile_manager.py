class ProfileManager:
    def __init__(self):
        self.profiles = {}

    def create_profile(self, username: str, interests: list) -> None:
        self.profiles[username] = {'interests': interests}
        self.save_profiles()

    def update_profile(self, username: str, interests: list) -> None:
        if username in self.profiles:
            self.profiles[username]['interests'] = interests
            self.save_profiles()

    def load_profiles(self) -> None:
        try:
            with open('profiles.txt', 'r') as file:
                for line in file:
                    username, interests = line.strip().split('|')
                    self.profiles[username] = {'interests': interests.split(',')}
        except FileNotFoundError:
            pass

    def save_profiles(self) -> None:
        with open('profiles.txt', 'w') as file:
            for username, profile in self.profiles.items():
                interests = ','.join(profile['interests'])
                file.write(f"{username}|{interests}\n")