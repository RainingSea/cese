import json

class PuzzleGenerator:
    def __init__(self, category: str):
        self.category = category
        self.puzzles = []
        self.load_puzzles()

    def load_puzzles(self) -> None:
        try:
            with open(f"{self.category}_puzzles.txt", "r") as file:
                self.puzzles = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"No puzzle file found for category: {self.category}")

    def generate_puzzle(self) -> str:
        if self.puzzles:
            return self.puzzles[0]  # For simplicity, just return the first puzzle
        return "No puzzles available"

    def check_solution(self, puzzle: str, solution: str) -> bool:
        # For simplicity, assume the solution is correct if it matches the puzzle
        return puzzle == solution