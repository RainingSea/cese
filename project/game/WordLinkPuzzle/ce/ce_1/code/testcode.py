import unittest
import os
from game import Game, Letter

class TestWordLinkPuzzleGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()

    def test_connect_letters_to_form_word(self):
        # Functionalities 1: Test connecting letters to form a word
        # Since the actual word validation logic is not implemented, we will fail this test
        self.fail("Word connection functionality is not implemented in the codebase")

    def test_scoring_system(self):
        # Functionalities 2: Test scoring system
        initial_score = self.game.score.get_score()
        self.game.score.calculate_score("DOG")
        self.assertEqual(self.game.score.get_score(), initial_score + 3, "Score should increase by 3 for the word 'DOG'")

    def test_timer_functionality(self):
        # Functionalities 3: Test timer functionality
        self.game.timer.start()
        time_before = self.game.timer.get_time()
        # Simulate a short wait
        time.sleep(1)
        time_after = self.game.timer.get_time()
        self.assertGreater(time_after, time_before, "Timer should increase over time")

    def test_difficulty_levels(self):
        # Functionalities 4: Test setting difficulty levels
        self.game.difficulty.set_level(2)  # Assume 2 is "Hard"
        self.assertEqual(self.game.difficulty.get_level(), 2, "Difficulty level should be set to 2")

    def test_save_progress(self):
        # Functionalities 5: Test saving progress
        self.game.score.calculate_score("CAT")  # Add some score
        self.game.save_progress()
        self.assertTrue(os.path.exists('progress.txt'), "Progress file should exist after saving")
        
        # Verify the contents of the progress file
        with open('progress.txt', 'r') as f:
            data = f.read().strip().split('|')
            self.assertEqual(int(data[0]), self.game.score.get_score(), "Saved score should match current score")
            self.assertEqual(int(data[1]), self.game.difficulty.get_level(), "Saved difficulty level should match current level")

    def test_load_saved_progress(self):
        # Functionalities 6: Test loading saved progress
        self.game.score.calculate_score("DOG")  # Change score
        self.game.save_progress()  # Save current progress
        self.game.score.points = 0  # Reset score to test loading
        self.game.load_progress()  # Load progress
        self.assertEqual(self.game.score.get_score(), 3, "Loaded score should match saved score")
        self.assertEqual(self.game.difficulty.get_level(), 1, "Loaded difficulty level should match saved level")

if __name__ == '__main__':
    unittest.main()
