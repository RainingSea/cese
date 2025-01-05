import json
from data_storage import DataStorage

class Job:
    def __init__(self, title: str, company: str, description: str):
        self.title = title
        self.company = company
        self.description = description
        self.data_storage = DataStorage()

    def post_job(self, title: str, company: str, description: str) -> bool:
        self.title = title
        self.company = company
        self.description = description
        return self.data_storage.save_job(self)

    def apply_job(self, username: str) -> bool:
        return self.data_storage.save_applied_job(username, self.title)