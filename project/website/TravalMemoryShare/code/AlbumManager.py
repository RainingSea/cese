import os

class AlbumManager:
    def __init__(self):
        self.albums = self.load_albums()

    def load_albums(self):
        if not os.path.exists('albums.txt'):
            return []
        with open('albums.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def create_album(self, user: str, album_data: dict) -> bool:
        album_entry = [user] + [album_data.get(key, '') for key in ['title', 'description', 'images']]
        self.albums.append(album_entry)
        self.save_albums()
        return True

    def save_albums(self):
        with open('albums.txt', 'w') as file:
            for album in self.albums:
                file.write('|'.join(album) + '\n')

    def customize_album(self, album_id: str, layout: dict) -> bool:
        # Customization functionality can be implemented here
        return True

    def explore_albums(self) -> list:
        return self.albums