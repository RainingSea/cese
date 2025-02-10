from file_manager import FileManager

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.file_manager = FileManager()

    def register(self) -> bool:
        users = self.file_manager.read_users()
        if any(username == self.username for username, _ in users):
            return False
        self.file_manager.write_user(self)
        return True

    def login(self) -> bool:
        users = self.file_manager.read_users()
        return any(username == self.username and password == self.password for username, password in users)