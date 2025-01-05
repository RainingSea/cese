import json
from data_storage import DataStorage

class User:
    def __init__(self, username: str, password: str, email: str = None):
        self.username = username
        self.password = password
        self.email = email
        self.data_storage = DataStorage()

    def register(self, username: str, password: str, email: str) -> bool:
        self.username = username
        self.password = password
        self.email = email
        return self.data_storage.save_user(self)

    def login(self, username: str, password: str) -> bool:
        users = self.data_storage.load_users()
        return username in users and users[username]['password'] == password

    def update_profile(self, email: str) -> bool:
        self.email = email
        return self.data_storage.save_user(self)