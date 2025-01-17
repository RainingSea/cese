import unittest
from game import Game, Timer, Progress

class TestWordLinkPuzzleGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_connect_letters_to_form_word(self):
        # Functionalities 1: Connect Letters to Form a Word
        selected_letters = [self.game.letters[2], self.game.letters[0], self.game.letters[19]]  # C, A, T
        self.game.connect_letters(selected_letters)
        # Check if the word "CAT" is recognized (assuming recognition means updating score)
        self.assertEqual(self.game.score, 3, "The word 'CAT' should be recognized and score updated.")

    def test_scoring_system(self):
        # Functionalities 2: Scoring System
        selected_letters = [self.game.letters[3], self.game.letters[14], self.game.letters[6]]  # D, O, G
        self.game.connect_letters(selected_letters)
        self.assertEqual(self.game.score, 3, "The player should receive 3 points for the word 'DOG'.")

    def test_timer_functionality(self):
        # Functionalities 3: Timer Functionality
        self.game.timer.start_timer(60)
        for _ in range(60):
            self.game.timer.update_timer()
        self.assertTrue(self.game.timer.is_time_up(), "The timer should count down correctly and be time up.")

    def test_difficulty_levels(self):
        # Functionalities 4: Difficulty Levels
        self.game.start_game("Hard")
        self.assertEqual(self.game.difficulty, "Hard", "The game should set the difficulty level to 'Hard'.")
        # Note: No specific rules for difficulty levels are implemented in the codebase.

    def test_save_progress(self):
        # Functionalities 5: Save Progress
        self.game.score = 10
        self.game.difficulty = "Medium"
        self.game.save_progress()
        with open('progress.txt', 'r') as f:
            content = f.read()
        self.assertIn("score|10", content, "The score should be saved in the progress file.")
        self.assertIn("difficulty|Medium", content, "The difficulty should be saved in the progress file.")

    def test_load_saved_progress(self):
        # Functionalities 6: Load Saved Progress
        with open('progress.txt', 'w') as f:
            f.write("score|15\ndifficulty|Hard\n")
        self.game.load_progress()
        self.assertEqual(self.game.score, 15, "The game should load the score from the saved progress.")
        self.assertEqual(self.game.difficulty, "Hard", "The game should load the difficulty from the saved progress.")

if __name__ == '__main__':
    unittest.main()
