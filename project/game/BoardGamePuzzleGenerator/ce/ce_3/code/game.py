import time
from puzzle_generator import PuzzleGenerator, Puzzle

class Game:
    def __init__(self):
        self.current_puzzle = None
        self.score = 0
        self.timer = 0

    def start_game(self, category: str) -> None:
        generator = PuzzleGenerator()
        generator.load_puzzles(f'puzzles/{category}.txt')
        self.current_puzzle = generator.get_random_puzzle()
        self.timer = time.time()

    def submit_solution(self, solution: str) -> bool:
        if self.current_puzzle.is_correct(solution):
            self.calculate_score()
            return True
        return False

    def calculate_score(self) -> int:
        self.score += 1
        return self.score