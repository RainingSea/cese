class ProfileManager:
    def __init__(self):
        self.profiles = self.load_profiles()

    def load_profiles(self):
        profiles = []
        with open('profiles.txt', 'r') as f:
            for line in f:
                username, interests = line.strip().split('|')
                profiles.append({'username': username, 'interests': interests})
        return profiles

    def create_profile(self, username: str, interests: str) -> bool:
        if any(profile['username'] == username for profile in self.profiles):
            return False
        self.profiles.append({'username': username, 'interests': interests})
        self.save_profiles()
        return True

    def update_profile(self, username: str, interests: str) -> bool:
        for profile in self.profiles:
            if profile['username'] == username:
                profile['interests'] = interests
                self.save_profiles()
                return True
        return False

    def save_profiles(self):
        with open('profiles.txt', 'w') as f:
            for profile in self.profiles:
                f.write(f"{profile['username']}|{profile['interests']}\n")