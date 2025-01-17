import unittest
import time
from game import Game
from puzzle_generator import PuzzleGenerator, Puzzle

class TestPuzzleGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.generator = PuzzleGenerator()

    def test_select_puzzle_category(self):
        # Functionalities 1: Select Puzzle Category
        try:
            self.game.start_game('logic_puzzles')
            self.assertIsNotNone(self.game.current_puzzle, "Puzzle should be generated for the selected category")
        except Exception as e:
            self.fail(f"Exception occurred: {e}")

    def test_generate_new_puzzle(self):
        # Functionalities 2: Generate a New Puzzle
        self.game.start_game('logic_puzzles')
        puzzle = self.game.current_puzzle
        self.assertIsInstance(puzzle, Puzzle, "A new puzzle should be generated and be an instance of Puzzle")

    def test_start_timer(self):
        # Functionalities 3: Start the Timer
        self.game.start_game('logic_puzzles')
        start_time = self.game.timer
        self.assertGreater(start_time, 0, "Timer should start when the game begins")

    def test_calculate_player_score(self):
        # Functionalities 4: Calculate Player’s Score
        self.game.start_game('logic_puzzles')
        self.game.submit_solution(self.game.current_puzzle.answer)
        self.assertEqual(self.game.score, 1, "Score should be incremented when the correct solution is submitted")

    def test_submit_solution(self):
        # Functionalities 5: Submit Solution
        self.game.start_game('logic_puzzles')
        correct = self.game.submit_solution(self.game.current_puzzle.answer)
        incorrect = self.game.submit_solution("wrong answer")
        self.assertTrue(correct, "Solution should be correct")
        self.assertFalse(incorrect, "Solution should be incorrect")

    def test_view_puzzle_feedback(self):
        # Functionalities 6: View Puzzle Feedback
        self.game.start_game('logic_puzzles')
        correct_feedback = self.game.submit_solution(self.game.current_puzzle.answer)
        incorrect_feedback = self.game.submit_solution("wrong answer")
        self.assertTrue(correct_feedback, "Feedback should indicate the solution is correct")
        self.assertFalse(incorrect_feedback, "Feedback should indicate the solution is incorrect")

    def test_timer_stops_on_solution_submission(self):
        # Functionalities 7: Timer Stops on Solution Submission
        self.game.start_game('logic_puzzles')
        time.sleep(1)  # Simulate time passing
        self.game.submit_solution(self.game.current_puzzle.answer)
        elapsed_time = time.time() - self.game.timer
        self.assertGreater(elapsed_time, 0, "Timer should stop and record the time taken to solve the puzzle")

    def test_load_puzzle_data_from_file(self):
        # Functionalities 8: Load Puzzle Data from File
        try:
            puzzles = self.generator.load_puzzles('puzzles/logic_puzzles.txt')
            self.assertGreater(len(puzzles), 0, "Puzzles should be loaded from the file")
        except FileNotFoundError:
            self.fail("Puzzle file not found")

    def test_validate_puzzle_solution_format(self):
        # Functionalities 9: Validate Puzzle Solution Format
        self.game.start_game('pattern_recognition')
        invalid_format = self.game.submit_solution("string instead of number")
        self.assertFalse(invalid_format, "Solution format should be validated and flagged as incorrect")

if __name__ == '__main__':
    unittest.main()
