import json
import random

class PuzzleGenerator:
    def __init__(self) -> None:
        self.puzzles = {}

    def load_puzzles(self, file_path: str) -> None:
        try:
            with open(file_path, 'r') as file:
                self.puzzles = json.load(file)
                self.validate_puzzles()
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading puzzles: {e}")

    def validate_puzzles(self) -> None:
        for category, puzzles in self.puzzles.items():
            if not isinstance(puzzles, list):
                raise ValueError(f"Category '{category}' does not contain a list of puzzles.")
            for puzzle in puzzles:
                if 'question' not in puzzle or 'answer' not in puzzle:
                    raise ValueError(f"Puzzle format is incorrect in category '{category}'.")

    def generate_puzzle(self, category: str, difficulty: str) -> dict:
        if category in self.puzzles and self.puzzles[category]:
            return random.choice(self.puzzles[category])
        else:
            return {"error": "No puzzles available in this category."}