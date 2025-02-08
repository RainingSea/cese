import json
import random

class PuzzleGenerator:
    def __init__(self):
        self.puzzles = []

    def load_puzzles(self, file_path: str) -> list:
        with open(file_path, 'r') as file:
            self.puzzles = [line.strip().split('|') for line in file.readlines()]
        return self.puzzles

    def get_random_puzzle(self) -> str:
        if not self.puzzles:
            raise ValueError("No puzzles loaded")
        question, answer = random.choice(self.puzzles)
        return Puzzle(question, answer)

class Puzzle:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer

    def is_correct(self, solution: str) -> bool:
        return self.answer.lower() == solution.lower()