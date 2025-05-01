import unittest
from game import Game

class TestNumberMysteryGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()
        self.game.load_puzzles()  # Load puzzles from the file

    def test_presenting_a_number_based_puzzle(self):
        # Functionalities 1: Check if a puzzle is loaded correctly
        self.assertGreater(len(self.game.puzzles), 0, "Puzzle should be loaded and displayed.")

    def test_deciphering_the_hidden_rule(self):
        # Functionalities 2: Check if the game confirms the correct rule
        self.game.current_level = 0  # Set to the first puzzle
        self.assertTrue(self.game.check_answer("Paris"), "The answer should be correct for the first puzzle.")

    def test_solving_the_puzzle(self):
        # Functionalities 3: Check if the puzzle can be solved
        self.game.current_level = 1  # Set to the second puzzle
        self.assertTrue(self.game.check_answer("4"), "The answer should be correct for the second puzzle.")

    def test_providing_feedback_on_progress(self):
        # Functionalities 4: Check feedback after solving a puzzle
        self.game.current_level = 0
        self.game.check_answer("Paris")  # Solve the first puzzle
        self.assertEqual(self.game.current_level, 1, "The level should be updated after solving the puzzle.")

    def test_tracking_level_completion(self):
        # Functionalities 5: Ensure level completion is tracked
        self.game.current_level = 0
        self.game.check_answer("Paris")  # Solve the first puzzle
        self.game.track_progress()
        with open('progress.txt', 'r') as file:
            progress = file.readline().strip().split('|')
            self.assertEqual(progress[0], '1', "Current level should be 1 after solving the first puzzle.")

    def test_using_hints(self):
        # Functionalities 6: Check if hints are provided correctly
        self.game.current_level = 0
        hint = self.game.get_hint()
        self.assertIn(hint, ["It is known as the city of lights.", "It is also a major European city."], 
                      "The hint should be valid for the first puzzle.")

    def test_handling_invalid_input(self):
        # Functionalities 7: Check if invalid input is handled
        self.game.current_level = 0
        self.assertFalse(self.game.check_answer("Wrong Answer"), "The answer should be incorrect.")

    def test_resetting_the_puzzle(self):
        # Functionalities 8: Check if the puzzle can be reset (not implemented in the codebase)
        self.fail("Resetting the puzzle functionality is not implemented in the codebase.")

    def test_storing_game_data(self):
        # Functionalities 9: Check if game data can be saved (not implemented in the codebase)
        self.fail("Storing game data functionality is not implemented in the codebase.")

    def test_loading_saved_game_data(self):
        # Functionalities 10: Check if game data can be loaded (not implemented in the codebase)
        self.fail("Loading saved game data functionality is not implemented in the codebase.")

if __name__ == '__main__':
    unittest.main()
