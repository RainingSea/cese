import unittest
from game import GameEngine
from score_manager import ScoreManager

class TestWordGridChallenge(unittest.TestCase):

    def setUp(self):
        # Initialize the game engine and score manager
        self.game_engine = GameEngine()
        self.score_manager = ScoreManager()
        self.score_manager.load_scores()  # Load existing scores if any

    def test_find_hidden_words(self):
        # Functionalities 1 Test finding a valid word "CAT"
        self.game_engine.grid.generate_grid(size=4)
        self.game_engine.grid.letters = [
            ['C', 'A', 'T', 'X'],
            ['X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X']
        ]
        self.assertTrue(self.game_engine.check_word("CAT"), "Should find the word 'CAT' in the grid")

        # Test finding an invalid word "CAG"
        self.assertFalse(self.game_engine.check_word("CAG"), "Should not find the word 'CAG' in the grid")

    def test_score_calculation(self):
        # Functionalities 2 Test score calculation
        self.score_manager.save_score("Alice", 100)
        self.score_manager.save_score("Bob", 150)
        self.assertEqual(self.score_manager.scores["Alice"], 100, "Alice's score should be 100")
        self.assertEqual(self.score_manager.scores["Bob"], 150, "Bob's score should be 150")

        # Simulate finding a longer word and check score
        self.score_manager.save_score("Charlie", 200)
        self.assertEqual(self.score_manager.scores["Charlie"], 200, "Charlie's score should be 200")

    def test_level_progression(self):
        # Functionalities 3 Test level progression (not implemented in codebase)
        self.fail("Level progression functionality is not implemented in the codebase")

    def test_timer_functionality(self):
        # Functionalities 4 Test timer functionality
        self.game_engine.timer.start()
        self.assertGreater(self.game_engine.timer.elapsed_time(), 0, "Timer should be running after starting the game")

    def test_data_storage(self):
        # Functionalities 5 Test saving game state (not implemented in codebase)
        self.fail("Save game state functionality is not implemented in the codebase")

        # Test loading game state (not implemented in codebase)
        self.fail("Load game state functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
