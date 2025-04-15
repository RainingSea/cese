from album import Album
from user import User

class Interaction:
    def __init__(self, album: Album):
        self.album = album
        self.likes = []
        self.comments = []

    def like(self, user: User):
        if user.username not in self.likes:
            self.likes.append(user.username)

    def comment(self, user: User, comment: str):
        self.comments.append((user.username, comment))

class InteractionController:
    def save_interaction(self, interaction: Interaction):
        with open('interactions.txt', 'a') as file:
            for like in interaction.likes:
                file.write(f"{interaction.album.title}|like|{like}\n")
            for comment in interaction.comments:
                file.write(f"{interaction.album.title}|comment|{comment[0]}|{comment[1]}\n")