from user import User
from album import Album
from interaction import Interaction

class Storage:
    def save_user(self, user: User):
        user.save()

    def save_album(self, album: Album):
        album.save()

    def save_interaction(self, interaction: Interaction):
        interaction.save()

    def load_users(self):
        users = []
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users.append(User(username, password))
        return users

    def load_albums(self):
        albums = []
        with open('albums.txt', 'r') as f:
            for line in f:
                user_id, title, description, photos = line.strip().split('|')
                album = Album(user_id, title, description)
                album.photos = photos.split(',') if photos else []
                albums.append(album)
        return albums

    def load_interactions(self):
        interactions = []
        with open('interactions.txt', 'r') as f:
            for line in f:
                user_id, album_id, type = line.strip().split('|')
                interactions.append(Interaction(user_id, album_id, type))
        return interactions