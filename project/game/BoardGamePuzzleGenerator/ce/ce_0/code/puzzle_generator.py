import random

class PuzzleGenerator:
    def __init__(self):
        self.puzzles = {}

    def load_puzzles(self, file_path: str) -> None:
        with open(file_path, 'r') as file:
            for line in file:
                category, puzzle = line.strip().split('|')
                if category not in self.puzzles:
                    self.puzzles[category] = []
                self.puzzles[category].append(puzzle)

    def generate_puzzle(self, category: str) -> str:
        if category in self.puzzles and self.puzzles[category]:
            return random.choice(self.puzzles[category])
        return "No puzzles available in this category."