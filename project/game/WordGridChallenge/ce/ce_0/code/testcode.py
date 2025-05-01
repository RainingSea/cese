import unittest
import pygame
from game import Game

class TestWordGridChallengeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()
        self.game.grid.generate_grid(5)  # Generate a grid of size 5 for testing
        self.game.word_list = ['CAT', 'DOG', 'MOUSE']  # Mock word list for testing

    def test_find_hidden_words(self):
        # Test finding a valid word "CAT"
        self.game.grid.letters = [
            ['C', 'A', 'T', 'X', 'Y'],
            ['D', 'O', 'G', 'Z', 'W'],
            ['M', 'O', 'U', 'S', 'E'],
            ['A', 'B', 'C', 'D', 'E'],
            ['F', 'G', 'H', 'I', 'J']
        ]
        found = self.game.grid.find_words()  # This should ideally contain logic to find words
        self.assertIn('CAT', found, "The word 'CAT' should be found in the grid")

        # Test finding an invalid word "CAG"
        found_invalid = self.game.grid.find_words()  # This should ideally contain logic to find words
        self.assertNotIn('CAG', found_invalid, "The word 'CAG' should not be found in the grid")

    def test_score_calculation(self):
        # Test score calculation after finding words
        self.game.update_score(10)  # Assume finding a word gives 10 points
        self.assertEqual(self.game.score.get_score(), 10, "Score should be 10 after finding one word")

        self.game.update_score(20)  # Assume finding another word gives 20 points
        self.assertEqual(self.game.score.get_score(), 30, "Score should be 30 after finding two words")

    def test_level_progression(self):
        # Test level progression (not implemented in codebase)
        self.fail("Level progression functionality is not implemented in the codebase")

    def test_timer_functionality(self):
        # Test timer starts when the game starts
        self.game.timer.start()
        elapsed_time = self.game.timer.get_elapsed_time()
        self.assertGreaterEqual(elapsed_time, 0, "Elapsed time should be greater than or equal to 0 after starting the timer")

    def test_data_storage(self):
        # Test saving score (mocking the file writing)
        self.game.save_score("Alice", 150)
        with open('scores.txt', 'r') as file:
            scores = file.readlines()
        self.assertIn("Alice|150\n", scores, "Score for Alice should be saved in scores.txt")

        # Test loading word list (mocking the file reading)
        self.assertGreater(len(self.game.word_list), 0, "Word list should be loaded and not empty")

if __name__ == '__main__':
    unittest.main()
