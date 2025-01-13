from FileManager import FileManager

class User:
    def __init__(self):
        self.file_manager = FileManager()

    def register(self, username: str, password: str) -> bool:
        users = self.file_manager.load_user_data()
        if username in users:
            return False
        self.file_manager.save_user_data(username, password)
        return True

    def login(self, username: str, password: str) -> bool:
        users = self.file_manager.load_user_data()
        return users.get(username) == password