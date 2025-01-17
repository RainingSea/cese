import unittest
from game import Game

class TestWordLinkPuzzle(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_connect_letters_to_form_word(self):
        # Functionalities 1: Connect Letters to Form a Word
        result = self.game.connect_letters(['C', 'A', 'T'])
        self.assertTrue(result, "The word 'CAT' should be recognized as a valid word")

    def test_scoring_system(self):
        # Functionalities 2: Scoring System
        initial_score = self.game.score.get_score()
        self.game.score.update_score(3)  # Simulate forming the word "DOG"
        self.assertEqual(self.game.score.get_score(), initial_score + 3, "Player should receive 3 points for the word 'DOG'")

    def test_timer_functionality(self):
        # Functionalities 3: Timer Functionality
        self.game.timer.start_timer(60)
        self.game.timer.update_timer()
        self.assertEqual(self.game.timer.time_remaining, 59, "Timer should count down correctly from the set time limit")

    def test_difficulty_levels(self):
        # Functionalities 4: Difficulty Levels
        self.game.difficulty.set_difficulty("Hard")
        self.assertEqual(self.game.difficulty.get_difficulty(), "Hard", "Game should set the difficulty level to 'Hard'")

    def test_save_progress(self):
        # Functionalities 5: Save Progress
        self.game.save_progress()
        with open('progress.txt', 'r') as f:
            content = f.read()
        self.assertIn(f"Score: {self.game.score.get_score()}", content, "Game state should be saved in a local text file")

    def test_load_saved_progress(self):
        # Functionalities 6: Load Saved Progress
        self.game.score.update_score(5)
        self.game.save_progress()
        self.game.score.points = 0  # Reset score to test loading
        self.game.load_progress()
        self.assertEqual(self.game.score.get_score(), 5, "Game should restore to the previous state accurately")

if __name__ == '__main__':
    unittest.main()
