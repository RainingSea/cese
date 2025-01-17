import unittest
from game import Game, Grid, Score, Timer

class TestWordGridChallenge(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.grid = self.game.grid
        self.score = self.game.score
        self.timer = self.game.timer

    def test_find_hidden_words_in_grid(self):
        # Functionalities 1: Find Hidden Words in the Grid
        self.grid.letters = [['C', 'A', 'T'], ['X', 'Y', 'Z'], ['P', 'Q', 'R']]
        self.grid.word_list = ['CAT']
        
        # Test finding a valid word "CAT"
        self.assertTrue(self.game.check_word("CAT"), "The word 'CAT' should be recognized as valid.")
        
        # Test finding an invalid word "CAG"
        self.assertFalse(self.game.check_word("CAG"), "The word 'CAG' should not be recognized as valid.")

    def test_score_calculation(self):
        # Functionalities 2: Score Calculation
        self.score.add_score(10)  # Simulate finding a word worth 10 points
        self.assertEqual(self.score.get_score(), 10, "Score should be 10 after adding 10 points.")
        
        self.score.add_score(20)  # Simulate finding another word worth 20 points
        self.assertEqual(self.score.get_score(), 30, "Score should be 30 after adding another 20 points.")

    def test_level_progression(self):
        # Functionalities 3: Level Progression
        self.game.start_game(0)
        initial_grid_size = len(self.grid.letters)
        
        self.game.start_game(1)
        new_grid_size = len(self.grid.letters)
        
        self.assertGreater(new_grid_size, initial_grid_size, "Grid size should increase with level progression.")

    def test_timer_functionality(self):
        # Functionalities 4: Timer Functionality
        self.timer.start_timer(60)
        self.assertEqual(self.timer.update_timer(), 59, "Timer should decrease by 1 second.")
        
        for _ in range(59):
            self.timer.update_timer()
        
        self.assertEqual(self.timer.update_timer(), 0, "Timer should reach zero after counting down.")

    def test_data_storage(self):
        # Functionalities 5: Data Storage
        self.fail("Save game state functionality is not implemented in the codebase")
        self.fail("Load game state functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
