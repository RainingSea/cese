import os

class DataHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def write_data(self, entry: str) -> None:
        with open(self.file_path, 'a') as file:
            file.write(entry + '\n')

    def read_data(self) -> list:
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r') as file:
            return file.readlines()