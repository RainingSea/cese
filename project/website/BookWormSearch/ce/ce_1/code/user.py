from data_storage import DataStorage

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.data_storage = DataStorage()

    def register(self, username: str, password: str) -> bool:
        users = self.data_storage.load_users()
        if any(user['username'] == username for user in users):
            return False
        users.append({'username': username, 'password': password})
        self.data_storage.save_users(users)
        return True

    def login(self, username: str, password: str) -> bool:
        users = self.data_storage.load_users()
        return any(user['username'] == username and user['password'] == password for user in users)