import pygame
from puzzle import PuzzleGenerator
from score import ScoreManager
from timer import Timer

class Game:
    def __init__(self):
        self.puzzle_generator = PuzzleGenerator()
        self.score_manager = ScoreManager()
        self.timer = Timer()
        self.current_puzzle = ""
        self.score = 0

    def start_game(self, category: str) -> None:
        self.puzzle_generator.load_puzzles()
        self.current_puzzle = self.puzzle_generator.generate_puzzle(category)
        self.timer.start()
        self.run_game_loop()

    def submit_solution(self, solution: str) -> None:
        time_taken = self.timer.stop()
        if solution == self.current_puzzle:  # Assuming the solution is the same as the puzzle for demo
            self.score = self.score_manager.calculate_score(time_taken, True)
            print("Correct! Your score:", self.score)
        else:
            self.score = self.score_manager.calculate_score(time_taken, False)
            print("Incorrect! Your score:", self.score)

    def run_game_loop(self):
        # Placeholder for game loop logic
        pass