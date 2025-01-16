from data_storage import DataStorage
import logging

class Profile:
    def __init__(self, username: str, interests: list):
        self.username = username
        self.interests = interests

    def update_profile(self, interests: list) -> bool:
        self.interests = interests
        storage = DataStorage()
        storage.save_profile(self)
        logging.info(f"Profile for {self.username} updated successfully.")
        return True