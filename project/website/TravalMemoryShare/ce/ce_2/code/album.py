from user import User

class Album:
    def __init__(self, title: str, owner: User, is_public: bool):
        self.title = title
        self.owner = owner
        self.images = []
        self.is_public = is_public

    def add_image(self, image_path: str):
        self.images.append(image_path)

    def customize_layout(self, layout: str):
        # Layout customization logic can be added here
        pass

    def share(self):
        # Logic for sharing the album can be added here
        pass

class AlbumController:
    def create_album(self, title: str, owner_username: str, is_public: bool):
        owner = User(owner_username, '')  # Password is not needed for album creation
        album = Album(title, owner, is_public)
        self.save_album(album)

    def save_album(self, album: Album):
        with open('albums.txt', 'a') as file:
            file.write(f"{album.title}|{album.owner.username}|{'|'.join(album.images)}|{album.is_public}\n")