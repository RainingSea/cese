import unittest
from game import Game
from score_storage import ScoreStorage
from word_list import WordList

class TestWordGridChallenge(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.word_list = WordList('word_list.txt')
        self.score_storage = ScoreStorage('scores.json')
        self.game.start_game()

    def test_find_hidden_words_in_grid(self):
        # Functionalities 1: Find Hidden Words in the Grid
        # Step: Start a new game with a predefined grid containing the word "CAT".
        self.game.grid = [['C', 'A', 'T'], ['D', 'O', 'G'], ['P', 'I', 'G']]
        
        # Expectation: The player can successfully connect the letters C, A, and T in the grid to form the word "CAT".
        self.assertTrue(self.game.check_word("CAT"), "The word 'CAT' should be recognized as valid.")
        
        # Expectation: Attempt to connect letters that do not form a valid word (e.g., C, A, G).
        self.assertFalse(self.game.check_word("CAG"), "The word 'CAG' should not be recognized as valid.")

    def test_score_calculation(self):
        # Functionalities 2: Score Calculation
        # Step: Complete a game by finding all the hidden words in the grid.
        self.game.update_score(10)  # Simulate finding a word worth 10 points
        self.game.update_score(20)  # Simulate finding another word worth 20 points
        
        # Expectation: The final score reflects the total points for all words found.
        self.assertEqual(self.game.score, 30, "The score should be 30 after finding words worth 10 and 20 points.")

    def test_level_progression(self):
        # Functionalities 3: Level Progression
        # Step: Complete the first level of the game.
        self.game.generate_grid(level=1)
        
        # Expectation: The player is automatically advanced to the next level with a larger grid.
        self.game.generate_grid(level=2)
        self.assertEqual(len(self.game.grid), 7, "The grid size should increase with level progression.")

    def test_timer_functionality(self):
        # Functionalities 4: Timer Functionality
        # Step: Start a new game and observe the timer.
        self.game.timer = 60
        
        # Expectation: The timer begins counting down as soon as the game starts.
        self.game.update_timer()
        self.assertLess(self.game.timer, 60, "The timer should count down from 60 seconds.")

    def test_data_storage(self):
        # Functionalities 5: Data Storage
        # Step: Save the game progress after completing a level.
        self.score_storage.save_score("player1", 100)
        
        # Expectation: The game state is correctly saved in a local text file.
        self.assertEqual(self.score_storage.scores["player1"], 100, "The score for player1 should be saved as 100.")

        # Step: Load a previously saved game.
        self.score_storage.scores = self.score_storage.load_scores()
        
        # Expectation: The game resumes from the saved state.
        self.assertIn("player1", self.score_storage.scores, "The saved score for player1 should be loaded.")

if __name__ == '__main__':
    unittest.main()
