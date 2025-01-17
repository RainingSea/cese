import unittest
from puzzle_generator import PuzzleGenerator
from timer import Timer
from scoring import Scoring

class TestPuzzleGame(unittest.TestCase):

    def setUp(self):
        # Initialize components for testing
        self.puzzle_generator = PuzzleGenerator("logic")
        self.timer = Timer()
        self.scoring = Scoring()

    def test_select_puzzle_category(self):
        # Functionalities 1: Select Puzzle Category
        self.assertEqual(self.puzzle_generator.category, "logic", "The selected category should be 'logic'.")

    def test_generate_new_puzzle(self):
        # Functionalities 2: Generate a New Puzzle
        puzzle = self.puzzle_generator.generate_puzzle()
        self.assertNotEqual(puzzle, "No puzzles available", "A puzzle should be generated and displayed.")

    def test_start_timer(self):
        # Functionalities 3: Start the Timer
        self.timer.start()
        self.assertGreater(self.timer.start_time, 0, "Timer should start counting up.")

    def test_calculate_player_score(self):
        # Functionalities 4: Calculate Player’s Score
        self.timer.start()
        time_taken = 240  # Simulate 4 minutes taken
        is_correct = True
        score = self.scoring.calculate_score(time_taken, is_correct)
        self.assertGreater(score, 0, "Score should be calculated based on time and accuracy.")

    def test_submit_solution(self):
        # Functionalities 5: Submit Solution
        puzzle = self.puzzle_generator.generate_puzzle()
        is_correct = self.puzzle_generator.check_solution(puzzle, puzzle)  # Simulate correct solution
        self.assertTrue(is_correct, "The solution should be correct.")

    def test_view_puzzle_feedback(self):
        # Functionalities 6: View Puzzle Feedback
        puzzle = self.puzzle_generator.generate_puzzle()
        is_correct = self.puzzle_generator.check_solution(puzzle, puzzle)  # Simulate correct solution
        feedback = "Correct" if is_correct else "Incorrect"
        self.assertEqual(feedback, "Correct", "Feedback should indicate the correctness of the solution.")

    def test_timer_stops_on_solution_submission(self):
        # Functionalities 7: Timer Stops on Solution Submission
        self.timer.start()
        self.timer.stop()
        self.assertGreater(self.timer.end_time, self.timer.start_time, "Timer should stop and record the final time.")

    def test_load_puzzle_data_from_file(self):
        # Functionalities 8: Load Puzzle Data from File
        self.puzzle_generator.load_puzzles()
        self.assertGreater(len(self.puzzle_generator.puzzles), 0, "Puzzle data should be loaded from the file.")

    def test_validate_puzzle_solution_format(self):
        # Functionalities 9: Validate Puzzle Solution Format
        puzzle = self.puzzle_generator.generate_puzzle()
        invalid_solution = "Invalid Format"
        is_correct = self.puzzle_generator.check_solution(puzzle, invalid_solution)
        self.assertFalse(is_correct, "The application should flag the submission as invalid.")

if __name__ == '__main__':
    unittest.main()
