class User:
    def __init__(self, username: str, password: str, bio: str = ""):
        self.username = username
        self.password = password
        self.bio = bio

    def update_bio(self, new_bio: str):
        self.bio = new_bio