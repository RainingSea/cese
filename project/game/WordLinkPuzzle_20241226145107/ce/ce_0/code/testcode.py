import unittest
from game import Game

class TestWordLinkPuzzleGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()
        self.game.dictionary.valid_words = {"CAT", "DOG", "APPLE", "BANANA", "CHERRY", "DATE", "FIG", "GRAPE"}

    def test_connect_letters_to_form_word(self):
        # Functionalities 1: Player connects letters "C", "A", "T" to form a word.
        self.game.grid.selected_letters = ['C', 'A', 'T']
        formed_word = ''.join(self.game.grid.selected_letters)
        self.assertTrue(self.game.dictionary.is_valid(formed_word), "The word 'CAT' should be recognized as valid.")

    def test_scoring_system(self):
        # Functionalities 2: Player forms the word "DOG" which is 3 letters long.
        word = "DOG"
        initial_score = self.game.score.get_score()
        self.game.update_score(word)
        new_score = self.game.score.get_score()
        self.assertEqual(new_score, initial_score + 3, "Player should receive 3 points for the word 'DOG'.")

    def test_timer_functionality(self):
        # Functionalities 3: Timer functionality is not implemented in the codebase
        self.fail("Timer functionality is not implemented in the codebase.")

    def test_difficulty_levels(self):
        # Functionalities 4: Difficulty levels are not implemented in the codebase
        self.fail("Difficulty levels functionality is not implemented in the codebase.")

    def test_save_progress(self):
        # Functionalities 5: Save progress functionality is not implemented in the codebase
        self.fail("Save progress functionality is not implemented in the codebase.")

    def test_load_saved_progress(self):
        # Functionalities 6: Load saved progress functionality is not implemented in the codebase
        self.fail("Load saved progress functionality is not implemented in the codebase.")

if __name__ == '__main__':
    unittest.main()
