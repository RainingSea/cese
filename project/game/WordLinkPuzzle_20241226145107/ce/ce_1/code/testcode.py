import unittest
from game import Game

class TestWordLinkPuzzleGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_connect_letters_to_form_word(self):
        # Functionalities 1: Player connects letters "C", "A", "T" to form a word.
        self.game.grid.connect_letters((200, 100))  # Assuming (200, 100) corresponds to 'C'
        self.game.grid.connect_letters((250, 100))  # Assuming (250, 100) corresponds to 'A'
        self.game.grid.connect_letters((300, 100))  # Assuming (300, 100) corresponds to 'T'
        formed_word = self.game.current_word
        self.assertEqual(formed_word, "CAT", "The word formed should be 'CAT'")
        self.assertTrue(self.game.dictionary.is_valid(formed_word), "The word 'CAT' should be recognized as valid")

    def test_scoring_system(self):
        # Functionalities 2: Player forms the word "DOG" which is 3 letters long.
        self.game.update_score("DOG")
        score = self.game.score.get_score()
        self.assertEqual(score, 3, "The score should be 3 points for the word 'DOG'")

    def test_timer_functionality(self):
        # Functionalities 3: Timer functionality is not implemented in the codebase
        self.fail("Timer functionality is not implemented in the codebase")

    def test_difficulty_levels(self):
        # Functionalities 4: Difficulty levels functionality is not implemented in the codebase
        self.fail("Difficulty levels functionality is not implemented in the codebase")

    def test_save_progress(self):
        # Functionalities 5: Save progress functionality is not implemented in the codebase
        self.fail("Save progress functionality is not implemented in the codebase")

    def test_load_saved_progress(self):
        # Functionalities 6: Load saved progress functionality is not implemented in the codebase
        self.fail("Load saved progress functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
