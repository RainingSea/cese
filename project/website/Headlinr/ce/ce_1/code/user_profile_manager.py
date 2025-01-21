class UserProfile:
    def __init__(self, username: str, preferences: list):
        self.username = username
        self.preferences = preferences
        self.bookmarks = []

class UserProfileManager:
    def __init__(self):
        self.profiles = self.load_profiles()

    def load_profiles(self):
        profiles = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, preferences = line.strip().split('|')
                profiles.append(UserProfile(username, preferences.split(',')))
        return profiles

    def create_profile(self, username: str, preferences: list):
        new_profile = UserProfile(username, preferences)
        self.profiles.append(new_profile)
        self.save_profiles()

    def save_profiles(self):
        with open('users.txt', 'w') as file:
            for profile in self.profiles:
                file.write(f"{profile.username}|{','.join(profile.preferences)}\n")

    def get_profile(self, username: str) -> UserProfile:
        for profile in self.profiles:
            if profile.username == username:
                return profile
        return None

    def update_profile(self, username: str, preferences: list):
        profile = self.get_profile(username)
        if profile:
            profile.preferences = preferences
            self.save_profiles()