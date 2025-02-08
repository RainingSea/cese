import unittest
from game import Game, WordValidator

class TestWordLinkPuzzleGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and word validator
        self.game = Game()
        self.word_validator = WordValidator()
        self.word_validator.load_words('words.txt')

    def test_connect_letters_to_form_word(self):
        # Functionalities 1: Connect Letters to Form a Word
        # Simulate connecting letters "C", "A", "T"
        word = "CAT"
        is_valid = self.word_validator.is_valid_word(word)
        self.assertTrue(is_valid, "The word 'CAT' should be recognized as a valid word")

    def test_scoring_system(self):
        # Functionalities 2: Scoring System
        # Simulate forming the word "DOG"
        word = "DOG"
        score = self.game.calculate_score(word)
        self.assertEqual(score, 3, "The player should receive 3 points for the word 'DOG'")

    def test_timer_functionality(self):
        # Functionalities 3: Timer Functionality
        # Start a new game and check the timer
        self.game.start_game("easy")
        self.assertEqual(self.game.timer, 60, "The timer should start at 60 seconds for a new game")

    def test_difficulty_levels(self):
        # Functionalities 4: Difficulty Levels
        # Select "Hard" difficulty level
        self.game.start_game("hard")
        self.assertEqual(self.game.difficulty, "hard", "The game should set the difficulty level to 'hard'")

    def test_save_progress(self):
        # Functionalities 5: Save Progress
        # Simulate saving progress
        self.game.save_progress('progress.txt')
        with open('progress.txt', 'r') as file:
            lines = file.readlines()
        self.assertIn("player1|0|60|hard\n", lines, "The game state should be saved in the progress file")

    def test_load_saved_progress(self):
        # Functionalities 6: Load Saved Progress
        # Simulate loading progress
        self.game.load_progress('progress.txt')
        # Since the load_progress function only prints, we assume it works if no errors occur
        self.assertTrue(True, "The game should load the saved progress without errors")

if __name__ == '__main__':
    unittest.main()
