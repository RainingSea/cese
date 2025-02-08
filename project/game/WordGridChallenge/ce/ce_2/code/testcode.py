import unittest
import os
from game import Game

class TestWordGridChallenge(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.game.load_words("words.txt")
        self.game.generate_grid(5)

    def test_find_hidden_words_in_grid(self):
        # Functionalities 1: Test finding a valid word
        self.game.grid = [['C', 'A', 'T'], ['A', 'B', 'C'], ['D', 'E', 'F']]
        self.assertTrue(self.game.check_word("CAT"), "Should recognize 'CAT' as a valid word")
        
        # Test finding an invalid word
        self.assertFalse(self.game.check_word("CAG"), "Should not recognize 'CAG' as a valid word")

    def test_score_calculation(self):
        # Functionalities 2: Test score calculation for valid words
        initial_score = self.game.score
        self.game.update_score(10)
        self.assertEqual(self.game.score, initial_score + 10, "Score should increase by 10 points")

        # Test score calculation for longer words
        self.game.update_score(20)
        self.assertEqual(self.game.score, initial_score + 30, "Score should increase by 20 more points")

    def test_level_progression(self):
        # Functionalities 3: Test level progression (not implemented in codebase)
        self.fail("Level progression functionality is not implemented in the codebase")

    def test_timer_functionality(self):
        # Functionalities 4: Test timer start
        self.game.start_timer()
        self.assertIsNotNone(self.game.timer, "Timer should start and not be None")

        # Test timer duration (not fully testable without game loop)
        elapsed_time = int(time.time() - self.game.timer)
        self.assertGreaterEqual(elapsed_time, 0, "Elapsed time should be non-negative")

    def test_data_storage(self):
        # Functionalities 5: Test saving game score
        self.game.update_score(50)
        self.game.save_score("TestPlayer")
        with open('scores.txt', 'r') as file:
            scores = file.readlines()
        self.assertIn("TestPlayer|50\n", scores, "Score should be saved in scores.txt")

        # Test loading game state (not implemented in codebase)
        self.fail("Load game state functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
