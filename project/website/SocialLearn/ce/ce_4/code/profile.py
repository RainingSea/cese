class Profile:
    def __init__(self, username: str, interests: list):
        self.username = username
        self.interests = interests

    def update(self, interests: list):
        self.interests = interests

    def save(self):
        with open('profiles.txt', 'a') as file:
            file.write(f"{self.username}|{','.join(self.interests)}\n")