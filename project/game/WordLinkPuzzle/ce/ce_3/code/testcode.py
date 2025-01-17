import unittest
from game import Game, Grid, Score, Timer, Difficulty

class TestWordLinkPuzzleGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.grid = self.game.grid
        self.score = self.game.score
        self.timer = self.game.timer
        self.difficulty = self.game.difficulty

    def test_connect_letters_to_form_word(self):
        # Functionalities 1: Connect Letters to Form a Word
        # Since the actual logic for word validation is not implemented, this test will fail
        result = self.grid.connect_letters((0, 0), (0, 2))  # Assume this connects "C", "A", "T"
        self.fail("Word validation logic is not implemented in the codebase")

    def test_scoring_system(self):
        # Functionalities 2: Scoring System
        initial_score = self.score.get_score()
        self.score.update_score(3)  # Simulate forming the word "DOG"
        self.assertEqual(self.score.get_score(), initial_score + 3, "Score should increase by the length of the word formed")

    def test_timer_functionality(self):
        # Functionalities 3: Timer Functionality
        self.timer.start_timer(60)
        for _ in range(10):
            self.timer.update_timer()
        self.assertEqual(self.timer.time_left, 50, "Timer should count down correctly")

    def test_difficulty_levels(self):
        # Functionalities 4: Difficulty Levels
        self.difficulty.set_difficulty("Hard")
        self.assertEqual(self.difficulty.get_difficulty(), "Hard", "Difficulty should be set to Hard")

    def test_save_progress(self):
        # Functionalities 5: Save Progress
        self.game.save_progress()
        with open('progress.txt', 'r') as file:
            lines = file.readlines()
            self.assertIn("Score: 0\n", lines, "Progress file should contain the current score")
            self.assertIn("Time Left: 60\n", lines, "Progress file should contain the current time left")

    def test_load_saved_progress(self):
        # Functionalities 6: Load Saved Progress
        self.game.save_progress()  # Ensure there is something to load
        self.game.load_progress()
        self.assertEqual(self.score.get_score(), 0, "Score should be loaded correctly from the file")
        self.assertEqual(self.timer.time_left, 60, "Time left should be loaded correctly from the file")

if __name__ == '__main__':
    unittest.main()
