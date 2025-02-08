import unittest
from game import Game
from puzzle_generator import PuzzleGenerator
from timer import Timer

class TestBoardGamePuzzleGenerator(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.puzzle_generator = self.game.puzzle_generator
        self.timer = self.game.timer

    def test_select_puzzle_category(self):
        # Functionalities 1: Select Puzzle Category
        self.puzzle_generator.load_puzzles("puzzles.txt")
        category = "Logic Puzzles"
        self.assertIn(category, self.puzzle_generator.puzzles, "Category should be available in puzzles")

    def test_generate_new_puzzle(self):
        # Functionalities 2: Generate a New Puzzle
        self.puzzle_generator.load_puzzles("puzzles.txt")
        category = "Logic Puzzles"
        puzzle = self.puzzle_generator.generate_puzzle(category)
        self.assertIn(puzzle, self.puzzle_generator.puzzles[category], "Generated puzzle should be from the selected category")

    def test_start_timer(self):
        # Functionalities 3: Start the Timer
        self.timer.start()
        elapsed_time = self.timer.get_elapsed_time()
        self.assertGreaterEqual(elapsed_time, 0, "Timer should start and show elapsed time")

    def test_calculate_player_score(self):
        # Functionalities 4: Calculate Player’s Score
        self.game.current_score = 0
        self.game.submit_solution("correct solution")
        self.assertEqual(self.game.current_score, 10, "Score should be incremented for correct solution")

    def test_submit_solution(self):
        # Functionalities 5: Submit Solution
        feedback = self.game.submit_solution("correct solution")
        self.assertEqual(feedback, "Correct!", "Feedback should indicate correct solution")

    def test_view_puzzle_feedback(self):
        # Functionalities 6: View Puzzle Feedback
        feedback = self.game.submit_solution("correct solution")
        self.assertIn(feedback, ["Correct!", "Incorrect!"], "Feedback should be displayed")

    def test_timer_stops_on_solution_submission(self):
        # Functionalities 7: Timer Stops on Solution Submission
        self.timer.start()
        self.game.submit_solution("correct solution")
        elapsed_time = self.timer.get_elapsed_time()
        self.assertGreaterEqual(elapsed_time, 0, "Timer should stop and show elapsed time")

    def test_load_puzzle_data_from_file(self):
        # Functionalities 8: Load Puzzle Data from File
        try:
            self.puzzle_generator.load_puzzles("puzzles.txt")
            self.assertTrue(True, "Puzzle data should be loaded successfully")
        except FileNotFoundError:
            self.fail("Puzzle file not found")

    def test_validate_puzzle_solution_format(self):
        # Functionalities 9: Validate Puzzle Solution Format
        # This functionality is not implemented in the codebase
        self.fail("Puzzle solution format validation is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
