import unittest
from unittest.mock import patch
from game import Game
from grid import Grid
from score import Score
from timer import Timer
from data_storage import DataStorage

class TestWordGridChallenge(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.grid = self.game.grid
        self.score = self.game.score
        self.timer = self.game.timer

    def test_find_hidden_words_in_grid(self):
        # Functionalities 1: Find Hidden Words in the Grid
        self.grid.letters = [['C', 'A', 'T'], ['A', 'B', 'C'], ['D', 'E', 'F']]
        self.game.word_list = ['CAT']
        
        # Test finding a valid word
        self.assertTrue(self.game.check_word('CAT'), "Should recognize 'CAT' as a valid word")
        self.game.update_score('CAT')
        self.assertEqual(self.score.get_score(), 3, "Score should be updated for finding 'CAT'")

        # Test finding an invalid word
        self.assertFalse(self.game.check_word('CAG'), "Should not recognize 'CAG' as a valid word")
        initial_score = self.score.get_score()
        self.game.update_score('CAG')
        self.assertEqual(self.score.get_score(), initial_score, "Score should not change for invalid word")

    def test_score_calculation(self):
        # Functionalities 2: Score Calculation
        self.grid.found_words = ['APPLE', 'BANANA']
        self.score.add_score(5)  # Assume 'APPLE' gives 5 points
        self.score.add_score(6)  # Assume 'BANANA' gives 6 points

        # Test final score calculation
        self.assertEqual(self.score.get_score(), 11, "Final score should reflect total points for all words found")

        # Test finding a longer word
        self.game.update_score('ELDERBERRY')
        self.assertEqual(self.score.get_score(), 21, "Score should increase appropriately for longer word 'ELDERBERRY'")

    def test_level_progression(self):
        # Functionalities 3: Level Progression
        # This functionality is not implemented in the codebase
        self.fail("Level progression functionality is not implemented in the codebase")

    def test_timer_functionality(self):
        # Functionalities 4: Timer Functionality
        self.timer.start_timer(60)
        self.assertEqual(self.timer.get_time(), 60, "Timer should start with 60 seconds")

        # Simulate timer countdown
        self.timer.time_left = 0
        self.assertEqual(self.timer.get_time(), 0, "Timer should reflect the countdown correctly")

    def test_data_storage(self):
        # Functionalities 5: Data Storage
        # This functionality is not implemented in the codebase
        self.fail("Data storage functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
