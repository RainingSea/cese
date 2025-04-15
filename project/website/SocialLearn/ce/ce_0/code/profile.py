class Profile:
    def __init__(self, username: str, interests: list):
        self.username = username
        self.interests = interests

    def save(self):
        """Save the profile to the profiles.txt file."""
        with open('profiles.txt', 'a') as file:
            file.write(f"{self.username}|{','.join(self.interests)}\n")

    @staticmethod
    def load_profiles() -> dict:
        """Load profiles from the profiles.txt file."""
        profiles = {}
        try:
            with open('profiles.txt', 'r') as file:
                for line in file:
                    username, interests = line.strip().split('|')
                    profiles[username] = interests.split(',')
        except FileNotFoundError:
            return {}
        return profiles