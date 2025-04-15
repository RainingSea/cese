class Profile:
    """Profile class to handle user profiles."""
    def __init__(self, username: str):
        self.username = username

    def update_profile(self, interests: list) -> bool:
        """Update user profile interests."""
        try:
            with open('profiles.txt', 'a') as file:
                file.write(f"{self.username}|{','.join(interests)}\n")
            return True
        except Exception as e:
            print(f"Error updating profile: {e}")
            return False

    def load_profile(self) -> dict:
        """Load all profiles from the profiles.txt file."""
        profiles = {}
        try:
            with open('profiles.txt', 'r') as file:
                for line in file:
                    username, interests = line.strip().split('|')
                    profiles[username] = interests.split(',')
        except Exception as e:
            print(f"Error loading profiles: {e}")
        return profiles