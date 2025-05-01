import random

class PuzzleGenerator:
    def __init__(self):
        self.puzzles = {}
        self.load_puzzles()

    def load_puzzles(self) -> None:
        categories = ['logic_puzzles.txt', 'pattern_recognition.txt', 'spatial_puzzles.txt']
        for category in categories:
            self.puzzles[category] = self.load_puzzle_data_from_file(category)

    def load_puzzle_data_from_file(self, filename: str) -> list:
        try:
            with open(filename, 'r') as file:
                return [line.strip() for line in file.readlines() if line.strip()]
        except FileNotFoundError:
            return []

    def generate_puzzle(self, category: str) -> str:
        return random.choice(self.puzzles.get(category, []))