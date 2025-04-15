import os

class Profile:
    def __init__(self, username: str):
        self.username = username
        self.interests = []

    def update(self, interests: list):
        self.interests = interests
        self.save()

    def save(self):
        with open('profiles.txt', 'a') as file:
            file.write(f"{self.username}|{','.join(self.interests)}\n")