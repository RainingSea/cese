import unittest
import json
from game import Game

class TestNumberMysteryGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and load data
        self.game = Game()
        self.game.load_data()

    def test_presenting_number_based_puzzle(self):
        # Functionalities 1: Presenting a Number-Based Puzzle
        # Load a puzzle and check if it is correctly loaded
        self.assertIn("puzzle1", self.game.puzzles, "Puzzle should be loaded")
        self.assertEqual(self.game.puzzles["puzzle1"]["question"], "What is 2 + 2?", "Puzzle question should match")

    def test_deciphering_hidden_rule(self):
        # Functionalities 2: Deciphering the Hidden Rule
        # This functionality is not implemented in the codebase
        self.fail("Deciphering the hidden rule functionality is not implemented in the codebase")

    def test_solving_the_puzzle(self):
        # Functionalities 3: Solving the Puzzle
        # Check if the solution is correct
        self.assertTrue(self.game.check_solution("4"), "The solution should be correct for puzzle1")

    def test_providing_feedback_on_progress(self):
        # Functionalities 4: Providing Feedback on Progress
        # This functionality is not implemented in the codebase
        self.fail("Providing feedback on progress functionality is not implemented in the codebase")

    def test_tracking_level_completion(self):
        # Functionalities 5: Tracking Level Completion
        # This functionality is not implemented in the codebase
        self.fail("Tracking level completion functionality is not implemented in the codebase")

    def test_using_hints(self):
        # Functionalities 6: Using Hints
        hint = self.game.provide_hint()
        self.assertEqual(hint, "Think about basic math.", "Hint should be provided for puzzle1")

    def test_handling_invalid_input(self):
        # Functionalities 7: Handling Invalid Input
        # Check if the solution is incorrect
        self.assertFalse(self.game.check_solution("5"), "The solution should be incorrect for puzzle1")

    def test_resetting_the_puzzle(self):
        # Functionalities 8: Resetting the Puzzle
        # This functionality is not implemented in the codebase
        self.fail("Resetting the puzzle functionality is not implemented in the codebase")

    def test_storing_game_data(self):
        # Functionalities 9: Storing Game Data
        self.game.save_progress()
        with open('progress.txt', 'r') as file:
            progress_data = file.read().strip()
        self.assertIn("player1|puzzle1", progress_data, "Progress should be saved correctly")

    def test_loading_saved_game_data(self):
        # Functionalities 10: Loading Saved Game Data
        self.game.load_progress()
        self.assertIn("player1", self.game.progress, "Progress should be loaded correctly")
        self.assertEqual(self.game.progress["player1"], "puzzle1", "Loaded progress should match the saved state")

if __name__ == '__main__':
    unittest.main()
