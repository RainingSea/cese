import unittest
from game import Game

class TestNumberMysteryGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()
        self.game.load_puzzles()  # Load puzzles from the file
        self.game.load_hints()     # Load hints from the file

    def test_presenting_number_based_puzzle(self):
        # Functionalities 1: Check if the puzzle is loaded correctly
        self.assertGreater(len(self.game.puzzles), 0, "Puzzle list should not be empty")
        self.assertIn('|', self.game.puzzles[0], "Puzzle format should contain '|'")

    def test_deciphering_hidden_rule(self):
        # Functionalities 2: Check if the answer is correct
        correct_answer = self.game.puzzles[self.game.current_level].split('|')[1]
        self.assertTrue(self.game.check_answer(correct_answer), "The answer should be correct")

    def test_solving_the_puzzle(self):
        # Functionalities 3: Check if the puzzle can be solved
        correct_answer = self.game.puzzles[self.game.current_level].split('|')[1]
        self.assertTrue(self.game.check_answer(correct_answer), "The puzzle should be solvable")

    def test_providing_feedback_on_progress(self):
        # Functionalities 4: Check if progress is updated correctly
        self.game.update_progress()
        with open('progress.txt', 'r') as file:
            content = file.readlines()
        self.assertIn(f"Level {self.game.current_level - 1} completed.\n", content, "Progress should be recorded in progress.txt")

    def test_tracking_level_completion(self):
        # Functionalities 5: Check if level completion updates correctly
        initial_level = self.game.current_level
        self.game.update_progress()
        self.assertEqual(self.game.current_level, initial_level + 1, "Current level should increment after completion")

    def test_using_hints(self):
        # Functionalities 6: Check if hints are provided correctly
        hint = self.game.provide_hint()
        self.assertIn(hint, self.game.hints, "Hint should be valid and present in hints list")

    def test_handling_invalid_input(self):
        # Functionalities 7: Check handling of invalid input
        self.assertFalse(self.game.check_answer("invalid_answer"), "The answer should be marked as incorrect")

    def test_resetting_the_puzzle(self):
        # Functionalities 8: Resetting the puzzle (not implemented in codebase)
        self.fail("Resetting the puzzle functionality is not implemented in the codebase")

    def test_storing_game_data(self):
        # Functionalities 9: Saving game data (not implemented in codebase)
        self.fail("Storing game data functionality is not implemented in the codebase")

    def test_loading_saved_game_data(self):
        # Functionalities 10: Loading saved game data (not implemented in codebase)
        self.fail("Loading saved game data functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
