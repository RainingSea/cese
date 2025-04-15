from user import User
from album import Album
from interaction import Interaction

class DataStorage:
    def save_user(self, user: User) -> None:
        user.save()

    def load_users(self) -> list:
        return User.load_users()

    def save_album(self, album: Album) -> None:
        with open('albums.txt', 'a') as file:
            file.write(f"{album.title}|{album.owner.username}|{'|'.join(album.images)}|{album.is_public}\n")

    def load_albums(self) -> list:
        albums = []
        try:
            with open('albums.txt') as file:
                for line in file:
                    title, owner, images, is_public = line.strip().split('|')
                    album = Album(title, User(owner, ''), is_public == 'True')
                    albums.append(album)
        except FileNotFoundError:
            pass
        return albums

    def save_interaction(self, interaction: Interaction) -> None:
        with open('interactions.txt', 'a') as file:
            for like in interaction.likes:
                file.write(f"{interaction.album.title}|like|{like}\n")
            for comment in interaction.comments:
                file.write(f"{interaction.album.title}|comment|{comment[0]}|{comment[1]}\n")

    def load_interactions(self) -> list:
        interactions = []
        try:
            with open('interactions.txt') as file:
                for line in file:
                    parts = line.strip().split('|')
                    if parts[1] == 'like':
                        interactions.append((parts[0], 'like', parts[2]))
                    elif parts[1] == 'comment':
                        interactions.append((parts[0], 'comment', parts[2], parts[3]))
        except FileNotFoundError:
            pass
        return interactions