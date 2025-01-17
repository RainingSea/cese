import json

class PuzzleGenerator:
    def __init__(self):
        self.puzzles = {
            'Logic': self.load_puzzles('logic_puzzles.txt'),
            'Pattern Recognition': self.load_puzzles('pattern_recognition_puzzles.txt'),
            'Spatial': self.load_puzzles('spatial_puzzles.txt')
        }

    def load_puzzles(self, filename: str) -> list:
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def generate_puzzle(self, category: str) -> str:
        if category in self.puzzles:
            return self.puzzles[category][0]  # Return the first puzzle for simplicity
        return "No puzzles available in this category."