import os

class FileHandler:
    @staticmethod
    def write_to_file(filename: str, data: str):
        with open(filename, 'a') as file:
            file.write(data + '\n')

    @staticmethod
    def read_from_file(filename: str) -> list:
        if not os.path.exists(filename):
            return []
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]