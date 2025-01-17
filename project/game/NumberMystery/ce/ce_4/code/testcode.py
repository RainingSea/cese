import unittest
from game import Game

class TestNumberMysteryGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and load puzzles
        self.game = Game()
        self.game.load_puzzles('puzzles.txt')

    def test_presenting_number_based_puzzle(self):
        # Functionalities 1: Test if the puzzle is presented correctly
        self.game.start_game()
        self.assertEqual(self.game.current_level, 0, "Game should start at level 0")
        self.assertEqual(self.game.puzzles[0].message, "Find the number that is the sum of 2 and 3", "First puzzle message should be displayed")

    def test_deciphering_hidden_rule(self):
        # Functionalities 2: Test if the correct rule allows progression
        self.game.start_game()
        self.assertTrue(self.game.submit_answer("5"), "Correct answer should allow progression to the next puzzle")

    def test_solving_puzzle(self):
        # Functionalities 3: Test solving the puzzle
        self.game.start_game()
        self.game.submit_answer("5")
        self.assertEqual(self.game.current_level, 1, "Game should progress to the next level after solving the puzzle")

    def test_providing_feedback_on_progress(self):
        # Functionalities 4: Test feedback on progress
        self.game.start_game()
        self.game.submit_answer("5")
        progress = self.game.get_progress()
        self.assertEqual(progress, "Current Level: 2/3", "Progress should reflect the current level after solving a puzzle")

    def test_tracking_level_completion(self):
        # Functionalities 5: Test level completion tracking
        self.game.start_game()
        self.game.submit_answer("5")
        self.assertEqual(self.game.current_level, 1, "Current level should update after completing a puzzle")

    def test_using_hints(self):
        # Functionalities 6: Test using hints
        self.game.start_game()
        hint = self.game.get_hint()
        self.assertEqual(hint, "The answer is more than 4", "Hint should be provided for the current puzzle")

    def test_handling_invalid_input(self):
        # Functionalities 7: Test handling invalid input
        self.game.start_game()
        result = self.game.submit_answer("4")
        self.assertFalse(result, "Incorrect answer should not allow progression")
        self.assertEqual(self.game.current_level, 0, "Level should not change on incorrect answer")

    def test_resetting_puzzle(self):
        # Functionalities 8: Test resetting the puzzle (not implemented in codebase)
        self.fail("Resetting puzzle functionality is not implemented in the codebase")

    def test_storing_game_data(self):
        # Functionalities 9: Test storing game data (not implemented in codebase)
        self.fail("Storing game data functionality is not implemented in the codebase")

    def test_loading_saved_game_data(self):
        # Functionalities 10: Test loading saved game data (not implemented in codebase)
        self.fail("Loading saved game data functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
