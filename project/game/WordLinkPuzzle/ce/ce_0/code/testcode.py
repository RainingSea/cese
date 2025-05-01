import unittest
import os
from main import Game, WordManager, ScoreManager

class TestWordLinkPuzzleGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.word_manager = WordManager()
        self.score_manager = ScoreManager()

    def test_form_word(self):
        # Functionalities 1: Connect Letters to Form a Word
        selected_letters = ['C', 'A', 'T']
        formed_word = self.word_manager.form_word(selected_letters)
        self.assertEqual(formed_word, 'CAT', "The word formed should be 'CAT'")
        self.assertTrue(self.word_manager.validate_word(formed_word), "The word 'CAT' should be recognized as valid")

    def test_scoring_system(self):
        # Functionalities 2: Scoring System
        word = "DOG"
        points = len(word)  # 3 points for 3 letters
        self.game.update_score(points)
        self.assertEqual(self.game.score, 3, "The score should be 3 after forming the word 'DOG'")

    def test_timer_functionality(self):
        # Functionalities 3: Timer Functionality
        initial_timer = self.game.timer
        self.assertEqual(initial_timer, 60, "The timer should start at 60 seconds")
        # Simulate timer countdown (not implemented in the codebase)
        self.fail("Timer countdown functionality is not implemented in the codebase")

    def test_difficulty_levels(self):
        # Functionalities 4: Difficulty Levels
        self.game.difficulty = 'hard'
        self.assertEqual(self.game.difficulty, 'hard', "The difficulty should be set to 'hard'")
        # Additional checks for rules can be added here (not implemented in the codebase)
        self.fail("Difficulty level rules are not implemented in the codebase")

    def test_save_progress(self):
        # Functionalities 5: Save Progress
        self.game.score = 10
        self.game.timer = 50
        self.game.difficulty = 'medium'
        self.game.save_progress()
        
        # Check if the progress.txt file is created and contains the correct data
        with open('progress.txt', 'r') as f:
            lines = f.readlines()
            self.assertEqual(lines[0].strip(), 'score|10', "Score should be saved as 10")
            self.assertEqual(lines[1].strip(), 'timer|50', "Timer should be saved as 50")
            self.assertEqual(lines[2].strip(), 'difficulty|medium', "Difficulty should be saved as 'medium'")

    def test_load_saved_progress(self):
        # Functionalities 6: Load Saved Progress
        self.game.score = 0  # Reset score
        self.game.load_progress()
        self.assertEqual(self.game.score, 10, "Score should be loaded as 10")
        self.assertEqual(self.game.timer, 50, "Timer should be loaded as 50")
        self.assertEqual(self.game.difficulty, 'medium', "Difficulty should be loaded as 'medium'")

if __name__ == '__main__':
    unittest.main()
