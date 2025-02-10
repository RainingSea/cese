class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.interests = []

    def update_profile(self, interests: list):
        self.interests = interests