import unittest
from game import Game, LetterGrid

class TestWordLinkPuzzle(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.letter_grid = self.game.letter_grid

    def test_connect_letters_to_form_word(self):
        # Functionalities 1: Connect Letters to Form a Word
        # Manually set the grid for a predictable test
        self.letter_grid.letters = [
            ['C', 'A', 'T', 'D', 'E'],
            ['F', 'G', 'H', 'I', 'J'],
            ['K', 'L', 'M', 'N', 'O'],
            ['P', 'Q', 'R', 'S', 'T'],
            ['U', 'V', 'W', 'X', 'Y']
        ]
        word = self.letter_grid.connect_letters((0, 0), (0, 2))
        self.assertEqual(word, "CAT", "The word formed should be 'CAT'")

    def test_scoring_system(self):
        # Functionalities 2: Scoring System
        initial_score = self.game.score.get_score()
        self.game.update_score("DOG")
        self.assertEqual(self.game.score.get_score(), initial_score + 3, "Score should increase by 3 points for the word 'DOG'")

    def test_timer_functionality(self):
        # Functionalities 3: Timer Functionality
        self.game.start_game()
        initial_time = self.game.timer.time_remaining
        self.game.timer.update_timer()
        self.assertEqual(self.game.timer.time_remaining, initial_time - 1, "Timer should count down by 1 second")

    def test_difficulty_levels(self):
        # Functionalities 4: Difficulty Levels
        self.game.difficulty.set_difficulty("Hard")
        self.assertEqual(self.game.difficulty.get_difficulty(), "Hard", "Difficulty should be set to 'Hard'")

    def test_save_progress(self):
        # Functionalities 5: Save Progress
        self.game.save_progress()
        with open('progress.txt', 'r') as f:
            lines = f.readlines()
            self.assertIn("Score:", lines[0], "Progress file should contain score")
            self.assertIn("Time Remaining:", lines[1], "Progress file should contain time remaining")

    def test_load_saved_progress(self):
        # Functionalities 6: Load Saved Progress
        self.game.save_progress()  # Ensure there's something to load
        self.game.score.points = 0  # Reset score
        self.game.timer.time_remaining = 0  # Reset timer
        self.game.load_progress()
        self.assertNotEqual(self.game.score.get_score(), 0, "Score should be restored from saved progress")
        self.assertNotEqual(self.game.timer.time_remaining, 0, "Time remaining should be restored from saved progress")

if __name__ == '__main__':
    unittest.main()
