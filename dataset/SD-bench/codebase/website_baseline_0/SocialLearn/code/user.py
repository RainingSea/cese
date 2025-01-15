from data_storage import DataStorage
import logging

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self) -> bool:
        storage = DataStorage()
        users = storage.load_users()
        if any(user.username == self.username for user in users):
            logging.warning(f"Registration failed: {self.username} already exists.")
            return False
        storage.save_user(self)
        logging.info(f"User {self.username} registered successfully.")
        return True

    def login(self) -> bool:
        storage = DataStorage()
        users = storage.load_users()
        if any(user.username == self.username and user.password == self.password for user in users):
            logging.info(f"User {self.username} logged in successfully.")
            return True
        logging.warning(f"Login failed for {self.username}.")
        return False