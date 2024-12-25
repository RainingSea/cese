import unittest
from game import Game

class TestWordLinkPuzzleGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_connect_letters_to_form_word(self):
        # Functionalities 1: Test connecting letters to form a word
        self.game.get_word_from_input = lambda: "CAT"  # Simulate input
        valid = self.game.validate_word("CAT")
        self.assertTrue(valid, "The word 'CAT' should be recognized as valid.")

    def test_scoring_system(self):
        # Functionalities 2: Test scoring system for the word "DOG"
        points = self.game.score.calculate_score("DOG")
        self.assertEqual(points, 3, "The player should receive 3 points for the word 'DOG'.")

    def test_timer_functionality(self):
        # Functionalities 3: Test timer functionality
        self.game.timer.start_timer(60)  # Start timer with 60 seconds
        initial_time = self.game.timer.time_left
        self.game.timer.update_timer()  # Simulate timer update
        self.assertEqual(self.game.timer.time_left, initial_time - 1, "Timer should count down correctly.")

    def test_difficulty_levels(self):
        # Functionalities 4: Test setting difficulty level
        self.game.start_game('Hard')
        grid_size = self.game.grid.get_grid_size('Hard')
        self.assertEqual(grid_size, 8, "The grid size for 'Hard' difficulty should be 8.")

    def test_save_progress(self):
        # Functionalities 5: Test saving progress
        self.game.score.add_points(10)  # Simulate scoring
        self.game.formed_words.add_word("CAT")  # Simulate forming a word
        self.game.timer.start_timer(30)  # Simulate timer
        self.game.save_progress()  # Save progress
        with open('game_state.txt', 'r') as f:
            lines = f.readlines()
            self.assertIn("Score: 10", lines[0], "Score should be saved correctly.")
            self.assertIn("Words: CAT", lines[1], "Formed words should be saved correctly.")
            self.assertIn("Time Left: 30", lines[2], "Time left should be saved correctly.")

    def test_load_saved_progress(self):
        # Functionalities 6: Test loading saved progress
        self.game.load_progress()  # Load progress
        self.assertEqual(self.game.score.get_score(), 0, "Score should be loaded correctly.")
        self.assertEqual(self.game.timer.time_left, 0, "Time left should be loaded correctly.")
        self.assertEqual(self.game.formed_words.get_words(), [], "Formed words should be loaded correctly.")

if __name__ == '__main__':
    unittest.main()
