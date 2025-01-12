from file_manager import FileManager

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self, username: str, password: str) -> bool:
        """Registers a new user if the username is not taken."""
        file_manager = FileManager()
        users = file_manager.load_user_data()
        if any(user.username == username for user in users):
            return False
        new_user = User(username, password)
        file_manager.save_user_data(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        """Logs in a user if credentials are correct."""
        file_manager = FileManager()
        users = file_manager.load_user_data()
        return any(user.username == username and user.password == password for user in users)