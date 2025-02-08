import unittest
from game import Game
from puzzle import PuzzleGenerator
from score import ScoreManager
from timer import Timer

class TestBoardGamePuzzleGenerator(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.puzzle_generator = self.game.puzzle_generator
        self.score_manager = self.game.score_manager
        self.timer = self.game.timer

    def test_select_puzzle_category(self):
        # Functionalities 1: Select Puzzle Category
        self.puzzle_generator.load_puzzles()
        category = "Logic Puzzles"
        self.game.start_game(category)
        self.assertEqual(self.game.current_puzzle in self.puzzle_generator.puzzles[category], True,
                         "The puzzle should be from the selected category.")

    def test_generate_new_puzzle(self):
        # Functionalities 2: Generate a New Puzzle
        self.puzzle_generator.load_puzzles()
        category = "Logic Puzzles"
        self.game.start_game(category)
        self.assertNotEqual(self.game.current_puzzle, "", "A new puzzle should be generated and not be empty.")

    def test_start_timer(self):
        # Functionalities 3: Start the Timer
        self.timer.start()
        self.assertGreater(self.timer.start_time, 0, "Timer should start and have a start time greater than 0.")

    def test_calculate_player_score(self):
        # Functionalities 4: Calculate Player’s Score
        self.timer.start()
        self.timer.start_time -= 240  # Simulate 4 minutes have passed
        self.game.submit_solution(self.game.current_puzzle)
        self.assertGreaterEqual(self.game.score, 60, "Score should be calculated based on time and accuracy.")

    def test_submit_solution(self):
        # Functionalities 5: Submit Solution
        self.timer.start()
        self.game.submit_solution(self.game.current_puzzle)
        self.assertIsInstance(self.game.score, int, "Score should be an integer after submitting a solution.")

    def test_view_puzzle_feedback(self):
        # Functionalities 6: View Puzzle Feedback
        self.timer.start()
        self.game.submit_solution("wrong solution")
        self.assertIsInstance(self.game.score, int, "Feedback should be provided and score should be an integer.")

    def test_timer_stops_on_solution_submission(self):
        # Functionalities 7: Timer Stops on Solution Submission
        self.timer.start()
        self.game.submit_solution(self.game.current_puzzle)
        time_taken = self.timer.stop()
        self.assertGreater(time_taken, 0, "Timer should stop and record the time taken.")

    def test_load_puzzle_data_from_file(self):
        # Functionalities 8: Load Puzzle Data from File
        try:
            self.puzzle_generator.load_puzzles()
            self.assertTrue(True, "Puzzle data should be loaded successfully.")
        except FileNotFoundError:
            self.fail("Puzzle data file not found.")

    def test_validate_puzzle_solution_format(self):
        # Functionalities 9: Validate Puzzle Solution Format
        # Assuming the solution should be a string for this test case
        invalid_solution = 12345  # An integer instead of a string
        with self.assertRaises(TypeError, msg="Solution format should be validated."):
            self.game.submit_solution(invalid_solution)

if __name__ == '__main__':
    unittest.main()
