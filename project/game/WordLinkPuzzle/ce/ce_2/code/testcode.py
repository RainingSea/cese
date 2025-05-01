import unittest
import json
import os
from game import Game
from score import Score
from timer import Timer
from difficulty import Difficulty

class TestWordLinkPuzzleGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.score = Score()
        self.timer = Timer()
        self.difficulty = Difficulty()

    def test_connect_letters_to_form_word(self):
        # Functionalities 1: Test connecting letters to form a word
        # This functionality is not implemented in the codebase
        self.fail("Connect letters functionality is not implemented in the codebase")

    def test_scoring_system(self):
        # Functionalities 2: Test scoring system
        word = "DOG"
        points = self.score.calculate_score(word)
        self.assertEqual(points, 3, "Player should receive 3 points for the word 'DOG'")

    def test_timer_functionality(self):
        # Functionalities 3: Test timer functionality
        self.timer.start_timer()
        time_remaining = self.timer.get_time()
        self.assertEqual(time_remaining, 60, "Timer should start at 60 seconds")
        
        # Simulate some time passing
        import time as time_module
        time_module.sleep(1)  # Sleep for 1 second
        time_remaining_after_sleep = self.timer.get_time()
        self.assertLess(time_remaining_after_sleep, 60, "Timer should count down correctly")

    def test_difficulty_levels(self):
        # Functionalities 4: Test setting difficulty levels
        self.difficulty.set_difficulty(3)  # Assuming 3 is 'Hard'
        self.assertEqual(self.difficulty.level, 3, "Difficulty level should be set to 3")

    def test_save_progress(self):
        # Functionalities 5: Test saving progress
        self.game.score.points = 10
        self.game.timer.duration = 50
        self.game.difficulty.level = 2
        self.game.save_progress()

        # Check if the progress file is created and contains correct data
        with open('progress.txt', 'r') as f:
            progress_data = json.load(f)
            self.assertEqual(progress_data['score'], 10, "Score should be saved as 10")
            self.assertEqual(progress_data['time_remaining'], 50, "Time remaining should be saved as 50")
            self.assertEqual(progress_data['difficulty_level'], 2, "Difficulty level should be saved as 2")

    def test_load_saved_progress(self):
        # Functionalities 6: Test loading saved progress
        self.game.load_progress()
        self.assertEqual(self.game.score.points, 0, "Score should be loaded as 0")
        self.assertEqual(self.game.timer.duration, 60, "Time remaining should be loaded as 60")
        self.assertEqual(self.game.difficulty.level, 1, "Difficulty level should be loaded as 1")

if __name__ == '__main__':
    unittest.main()
