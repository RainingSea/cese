from data_manager import DataManager, Album, Comment

class AlbumManager:
    def __init__(self):
        self.data_manager = DataManager()
        self.albums = self.data_manager.load_albums()
        self.comments = self.data_manager.load_comments()  # Load comments for future use
        self.user_manager = UserManager()  # Initialize UserManager for notifications

    def create_album(self, title: str, owner: str, images: list, is_private: bool) -> bool:
        new_album = Album(title, owner, images, is_private)
        self.data_manager.save_album(new_album)
        self.albums.append(new_album)
        self.user_manager.notify_users_of_new_album(title, owner)  # Notify followers
        return True

    def get_albums(self) -> list:
        return self.albums

    def add_comment(self, album_id: str, user: str, content: str) -> bool:
        new_comment = Comment(album_id, user, content)
        self.data_manager.save_comment(new_comment)
        return True

    def explore_albums(self) -> list:
        return self.get_albums()

    def share_album(self, album_id: str, shared_with: List[str]) -> bool:
        self.data_manager.share_album(album_id, shared_with)
        return True