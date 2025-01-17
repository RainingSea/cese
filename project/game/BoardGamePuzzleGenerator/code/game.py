import pygame
from puzzle_generator import PuzzleGenerator
from scoring import ScoreManager
from timer import Timer

class Game:
    def __init__(self) -> None:
        self.puzzle_generator = PuzzleGenerator()
        self.score_manager = ScoreManager()
        self.timer = Timer()
        self.current_score = 0
        self.last_puzzle = None

    def start_game(self, category: str, difficulty: str) -> None:
        try:
            self.puzzle_generator.load_puzzles("puzzles.json")
            self.timer.start()
            self.last_puzzle = self.puzzle_generator.generate_puzzle(category, difficulty)
            if "error" not in self.last_puzzle:
                print(f"Puzzle: {self.last_puzzle['question']}")  # Display the question
            else:
                print(self.last_puzzle["error"])
        except Exception as e:
            print(f"An error occurred while starting the game: {e}")

    def submit_solution(self, solution: str) -> None:
        if not self.validate_solution_format(solution):
            print("Invalid solution format. Please try again.")
            return
        
        elapsed_time = self.timer.stop()
        print(f"Elapsed Time: {elapsed_time:.2f} seconds")
        self.timer.start()  # Reset timer for next puzzle

        feedback = self.check_solution(solution)
        if feedback['correct']:
            self.current_score += 10  # Increment score for correct answer
            self.score_manager.update_score("player", self.current_score)
            print("Correct!")
        else:
            print(f"Incorrect! The correct answer was: {feedback['correct_answer']}")

    def check_solution(self, solution: str) -> dict:
        if solution == self.last_puzzle['answer']:
            return {'correct': True}
        else:
            return {'correct': False, 'correct_answer': self.last_puzzle['answer']}

    def validate_solution_format(self, solution: str) -> bool:
        return isinstance(solution, str) and len(solution.strip()) > 0