from data_manager import DataManager, User, Notification

class UserManager:
    def __init__(self):
        self.data_manager = DataManager()
        self.users = self.data_manager.load_users()

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False  # User already exists
        new_user = User(username, password)
        self.data_manager.save_user(new_user)
        self.users.append(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user.username == username and user.password == password for user in self.users)

    def get_shared_albums(self, username: str) -> List[str]:
        shared_albums = self.data_manager.load_shared_albums()
        return [album_id for album_id, users in shared_albums if username in users]

    def follow_user(self, follower: str, followee: str) -> bool:
        if any(user.username == followee for user in self.users):
            self.data_manager.follow_user(follower, followee)
            return True
        return False

    def get_followers(self, username: str) -> List[str]:
        return self.data_manager.load_followers(username)

    def notify_users_of_new_album(self, album_title: str, owner: str):
        followers = self.get_followers(owner)
        for follower in followers:
            message = f"{owner} has created a new album: {album_title}"
            notification = Notification(follower, message)
            self.data_manager.save_notification(notification)