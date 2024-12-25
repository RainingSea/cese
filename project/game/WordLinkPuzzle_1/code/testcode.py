import unittest
from game import Game

class TestWordLinkPuzzleGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()

    def test_grid_generation(self):
        # Functionalities 1 Test grid generation
        self.game.grid.generate_grid(4)
        self.assertEqual(len(self.game.grid.letters), 4, "Grid should have 4 rows")
        self.assertEqual(len(self.game.grid.letters[0]), 4, "Grid should have 4 columns")

    def test_word_validation(self):
        # Functionalities 2 Test word validation against the dictionary
        valid_word = "APPLE"
        invalid_word = "INVALID"
        self.assertTrue(self.game.grid.validate_word(valid_word), "APPLE should be a valid word")
        self.assertFalse(self.game.grid.validate_word(invalid_word), "INVALID should not be a valid word")

    def test_score_calculation(self):
        # Functionalities 3 Test score calculation
        word = "BANANA"
        score = self.game.score.calculate_score(word)
        self.assertEqual(score, 6, "Score for BANANA should be 6 (6 for length + 0 bonus)")

        long_word = "EXTRAORDINARY"
        long_score = self.game.score.calculate_score(long_word)
        self.assertEqual(long_score, 15, "Score for EXTRAORDINARY should be 15 (13 for length + 5 bonus)")

    def test_add_points(self):
        # Functionalities 4 Test adding points to score
        self.game.score.add_points(10)
        self.assertEqual(self.game.score.get_score(), 10, "Score should be 10 after adding 10 points")

    def test_timer_functionality(self):
        # Functionalities 5 Test timer functionality
        self.game.timer.start_timer(60)
        self.assertEqual(self.game.timer.time_left, 60, "Timer should start with 60 seconds")
        self.game.timer.update_timer()
        self.assertEqual(self.game.timer.time_left, 59, "Timer should decrement by 1 second")

    def test_pause_resume_timer(self):
        # Functionalities 6 Test pause and resume timer
        self.game.timer.start_timer(60)
        self.game.timer.pause_timer()
        time_left_before_update = self.game.timer.time_left
        self.game.timer.update_timer()
        self.assertEqual(self.game.timer.time_left, time_left_before_update, "Timer should not decrement while paused")

        self.game.timer.resume_timer()
        self.game.timer.update_timer()
        self.assertEqual(self.game.timer.time_left, time_left_before_update - 1, "Timer should decrement after resuming")

    def test_save_game_state(self):
        # Functionalities 7 Test saving game state
        self.game.save_game()
        with open('game_state.txt', 'r') as file:
            lines = file.readlines()
            self.assertEqual(len(lines), 4, "Game state should save 4 lines of data")

    def test_load_game_state(self):
        # Functionalities 8 Test loading game state
        self.game.load_game()
        self.assertEqual(len(self.game.grid.letters), 4, "Loaded grid should have 4 rows")
        self.assertEqual(self.game.score.get_score(), 0, "Loaded score should be 0")
        self.assertEqual(self.game.timer.time_left, 60, "Loaded timer should have 60 seconds")
        self.assertEqual(len(self.game.formed_words.get_words()), 0, "Loaded words should be empty")

    def test_play_sound(self):
        # Functionalities 9 Test play sound functionality (not implemented in codebase)
        self.fail("Play sound functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
