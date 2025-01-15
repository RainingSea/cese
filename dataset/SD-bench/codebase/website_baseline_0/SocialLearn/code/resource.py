from data_storage import DataStorage
import logging

class Resource:
    def __init__(self, title: str, link: str):
        self.title = title
        self.link = link

    def share_resource(self) -> bool:
        storage = DataStorage()
        storage.save_resource(self)
        logging.info(f"Resource {self.title} shared successfully.")
        return True