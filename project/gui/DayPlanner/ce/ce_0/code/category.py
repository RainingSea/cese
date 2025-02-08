import os

class Category:
    def __init__(self, name: str):
        self.name = name

    def save(self):
        with open('categories.txt', 'a') as file:
            file.write(f"{self.name}\n")

    @staticmethod
    def load() -> list:
        if not os.path.exists('categories.txt'):
            return []
        with open('categories.txt', 'r') as file:
            categories = [line.strip() for line in file.readlines()]
        return categories