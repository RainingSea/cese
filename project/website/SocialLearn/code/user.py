class User:
    def __init__(self, username, password, interests=None):
        self.username = username
        self.password = password
        self.interests = interests if interests is not None else []

    def create_profile(self, username, password, interests):
        self.username = username
        self.password = password
        self.interests = interests

    def update_profile(self, interests):
        self.interests = interests