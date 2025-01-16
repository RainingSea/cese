class AlbumManager:
    def __init__(self):
        self.albums = self.load_albums()

    def load_albums(self):
        albums = []
        with open('albums.txt', 'r') as file:
            for line in file:
                album_data = line.strip().split('|')
                albums.append({
                    'user': album_data[0],
                    'title': album_data[1],
                    'photos': album_data[2].split(','),
                    'privacy': album_data[3]
                })
        return albums

    def create_album(self, user: str, album_data: dict) -> None:
        self.albums.append(album_data)
        with open('albums.txt', 'a') as file:
            photos_str = ','.join(album_data['photos'])
            file.write(f"{user}|{album_data['title']}|{photos_str}|{album_data['privacy']}\n")

    def share_album(self, album_id: str, privacy: str) -> None:
        pass  # Sharing functionality can be added later

    def like_album(self, album_id: str, user: str) -> None:
        pass  # Liking functionality can be added later

    def comment_on_album(self, album_id: str, user: str, comment: str) -> None:
        pass  # Commenting functionality can be added later

    def explore_albums(self) -> list:
        return self.albums