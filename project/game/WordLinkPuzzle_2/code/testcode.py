import unittest
from game import Game

class TestWordLinkPuzzleGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()

    def test_grid_generation(self):
        # Functionalities 1: Test grid generation
        self.game.grid.generate_grid(4)
        grid = self.game.grid.get_letters()
        self.assertEqual(len(grid), 4, "Grid should have 4 rows")
        self.assertTrue(all(len(row) == 4 for row in grid), "Each row in the grid should have 4 letters")

    def test_score_update(self):
        # Functionalities 2: Test score update based on word length
        initial_score = self.game.score.get_score()
        self.game.score.update_score("APPLE")
        self.assertEqual(self.game.score.get_score(), initial_score + 5, "Score should increase by 5 for the word 'APPLE'")

        self.game.score.update_score("BANANA")
        self.assertEqual(self.game.score.get_score(), initial_score + 11, "Score should increase by 11 for the word 'BANANA'")

    def test_bonus_score(self):
        # Functionalities 3: Test bonus score for complex words
        initial_score = self.game.score.get_score()
        self.game.score.update_score("ORANGE")
        self.assertEqual(self.game.score.get_score(), initial_score + 7, "Score should increase by 7 for the word 'ORANGE' (including bonus)")

    def test_timer_functionality(self):
        # Functionalities 4: Test timer start and decrement
        self.game.timer.start_timer(10)
        self.assertEqual(self.game.timer.check_time(), 10, "Timer should start at 10 seconds")
        self.game.timer.decrement_time()
        self.assertEqual(self.game.timer.check_time(), 9, "Timer should decrement by 1 second")

    def test_pause_and_resume_timer(self):
        # Functionalities 5: Test pause and resume functionality
        self.game.timer.start_timer(10)
        self.game.timer.pause_timer()
        self.assertTrue(self.game.timer.is_paused, "Timer should be paused")
        self.game.timer.resume_timer()
        self.assertFalse(self.game.timer.is_paused, "Timer should be resumed")

    def test_validate_word(self):
        # Functionalities 6: Test word validation
        self.assertTrue(self.game.validate_word("APPLE"), "APPLE should be a valid word")
        self.assertFalse(self.game.validate_word("INVALID"), "INVALID should not be a valid word")

    def test_save_progress(self):
        # Functionalities 7: Test saving game progress (not implemented in codebase)
        self.fail("Save progress functionality is not implemented in the codebase")

    def test_load_progress(self):
        # Functionalities 8: Test loading game progress (not implemented in codebase)
        self.fail("Load progress functionality is not implemented in the codebase")

    def test_play_word_formed_sound(self):
        # Functionalities 9: Test playing sound when a word is formed (not implemented in codebase)
        self.fail("Play word formed sound functionality is not implemented in the codebase")

    def test_play_bonus_points_sound(self):
        # Functionalities 10: Test playing bonus points sound (not implemented in codebase)
        self.fail("Play bonus points sound functionality is not implemented in the codebase")

    def test_play_timer_warning_sound(self):
        # Functionalities 11: Test playing timer warning sound (not implemented in codebase)
        self.fail("Play timer warning sound functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
