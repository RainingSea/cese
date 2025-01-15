from data_storage import DataStorage
import logging

class Message:
    def __init__(self, sender: str, receiver: str, content: str):
        self.sender = sender
        self.receiver = receiver
        self.content = content

    def send_message(self) -> bool:
        storage = DataStorage()
        storage.save_message(self)
        logging.info(f"Message sent from {self.sender} to {self.receiver}.")
        return True