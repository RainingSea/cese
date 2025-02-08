import time
from puzzles import PuzzleGenerator

class Timer:
    def __init__(self):
        self.start_time = 0.0

    def start(self):
        self.start_time = time.time()

    def get_elapsed_time(self) -> float:
        return time.time() - self.start_time

class Score:
    def __init__(self):
        self.points = 0

    def calculate_score(self, time_taken: float, is_correct: bool) -> int:
        if is_correct:
            self.points += max(0, 100 - int(time_taken * 10))  # Simple scoring logic
        return self.points

    def get_score(self) -> int:
        return self.points

class Game:
    def __init__(self):
        self.puzzle_generator = PuzzleGenerator()
        self.timer = Timer()
        self.score = Score()

    def start_game(self, category: str):
        self.timer.start()
        puzzle = self.puzzle_generator.generate_puzzle(category)
        print(f"Puzzle: {puzzle}")

    def submit_solution(self, solution: str) -> bool:
        # Here we would check the solution against the correct answer
        # For simplicity, we will assume the solution is always correct
        is_correct = True
        time_taken = self.timer.get_elapsed_time()
        self.score.calculate_score(time_taken, is_correct)
        return is_correct