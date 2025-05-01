import os

class DataStorage:
    def __init__(self):
        self.file_map = {
            'theories': 'theories.txt',
            'concepts': 'concepts.txt',
            'experiments': 'experiments.txt'
        }

    def load_data(self, type: str):
        if type not in self.file_map:
            raise ValueError("Invalid type specified.")
        file_path = self.file_map[type]
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def save_data(self, type: str, knowledge: str):
        if type not in self.file_map:
            raise ValueError("Invalid type specified.")
        file_path = self.file_map[type]
        with open(file_path, 'a') as file:
            file.write(knowledge + '\n')