import unittest
from game import Game

class TestWordGridChallenge(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()
        self.game.start_game()

    def test_find_hidden_words_in_grid(self):
        # Functionalities 1: Test finding a valid word "CAT"
        self.game.grid.letters = [
            ['C', 'A', 'T', 'D'],
            ['E', 'F', 'G', 'H'],
            ['I', 'J', 'K', 'L'],
            ['M', 'N', 'O', 'P']
        ]
        self.assertTrue(self.game.check_word_selection(['C', 'A', 'T']), "Should recognize 'CAT' as a valid word")
        initial_score = self.game.score.get_score()
        self.game.update_score('CAT')
        self.assertEqual(self.game.score.get_score(), initial_score + 3, "Score should increase by 3 for 'CAT'")

        # Test finding an invalid word "CAG"
        self.assertFalse(self.game.check_word_selection(['C', 'A', 'G']), "Should not recognize 'CAG' as a valid word")
        self.assertEqual(self.game.score.get_score(), initial_score + 3, "Score should remain unchanged for 'CAG'")

    def test_score_calculation(self):
        # Functionalities 2: Test score calculation for multiple words
        self.game.update_score('APPLE')
        self.game.update_score('BANANA')
        self.assertEqual(self.game.score.get_score(), 11, "Score should be 11 after finding 'APPLE' and 'BANANA'")

        # Test finding a longer word
        self.game.update_score('CHERRY')
        self.assertEqual(self.game.score.get_score(), 17, "Score should increase by 6 for 'CHERRY'")

    def test_level_progression(self):
        # Functionalities 3: Test level progression (not implemented in codebase)
        self.fail("Level progression functionality is not implemented in the codebase")

    def test_timer_functionality(self):
        # Functionalities 4: Test timer functionality
        self.game.timer.start()
        time_elapsed = self.game.timer.get_time_elapsed()
        self.assertGreaterEqual(time_elapsed, 0, "Timer should start counting time")

    def test_data_storage(self):
        # Functionalities 5: Test data storage (not implemented in codebase)
        self.fail("Data storage functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
