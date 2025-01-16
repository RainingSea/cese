class Profile:
    def __init__(self, username: str, interests: list):
        self.username = username
        self.interests = interests

    def update(self, interests: list):
        self.interests = interests

    def save(self):
        pass  # Saving handled in main.py