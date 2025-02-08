import random

class PuzzleGenerator:
    def __init__(self):
        self.puzzles = {
            "Logic Puzzles": [],
            "Pattern Recognition": [],
            "Spatial Puzzles": []
        }

    def load_puzzles(self) -> None:
        for category in self.puzzles.keys():
            with open(f'puzzles/{category.lower().replace(" ", "_")}_puzzles.txt', 'r') as file:
                self.puzzles[category] = [line.strip() for line in file.readlines()]

    def generate_puzzle(self, category: str) -> str:
        return random.choice(self.puzzles[category]) if self.puzzles[category] else ""