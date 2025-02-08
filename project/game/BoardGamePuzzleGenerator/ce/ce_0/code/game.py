import pygame
from puzzle_generator import PuzzleGenerator
from score_manager import ScoreManager
from timer import Timer

class Game:
    def __init__(self):
        self.puzzle_generator = PuzzleGenerator()
        self.score_manager = ScoreManager()
        self.timer = Timer()
        self.current_score = 0

    def start_game(self, category: str) -> None:
        self.puzzle_generator.load_puzzles("puzzles.txt")
        puzzle = self.puzzle_generator.generate_puzzle(category)
        self.timer.start()
        self.display_puzzle(puzzle)

    def display_puzzle(self, puzzle: str) -> None:
        # Placeholder for displaying puzzle on screen
        print(f"Puzzle: {puzzle}")

    def submit_solution(self, solution: str) -> str:
        elapsed_time = self.timer.get_elapsed_time()
        self.timer.start()  # Reset timer for next puzzle
        # Placeholder for checking solution
        correct = True  # Simulating correct solution check
        if correct:
            self.current_score += 10  # Increment score for correct answer
            return "Correct!"
        else:
            return "Incorrect!"