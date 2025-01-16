from data_storage import DataStorage
import logging

class StudyGroup:
    def __init__(self, group_name: str, members: list):
        self.group_name = group_name
        self.members = members

    def join_group(self, username: str) -> bool:
        if username not in self.members:
            self.members.append(username)
            storage = DataStorage()
            storage.save_group(self)
            logging.info(f"User {username} joined group {self.group_name}.")
            return True
        logging.warning(f"User {username} already in group {self.group_name}.")
        return False