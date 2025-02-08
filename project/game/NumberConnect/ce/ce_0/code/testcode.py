import unittest
from game import Game

class TestNumberConnectGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_connect_numbers_in_sequence(self):
        # Functionality 1: Connect Numbers in Sequence
        self.game.start_game(3)
        # Simulate clicking on numbers in sequence
        valid_sequence = [(0, 0), (0, 1), (0, 2), (1, 2), (1, 1), (1, 0), (2, 0), (2, 1), (2, 2)]
        for i in range(len(valid_sequence) - 1):
            current_pos = valid_sequence[i]
            next_pos = valid_sequence[i + 1]
            self.assertTrue(self.game.check_move(current_pos, next_pos), "The path should be valid.")

        self.game.start_game(4)
        # Simulate clicking on a non-adjacent tile
        self.assertFalse(self.game.check_move((0, 0), (2, 2)), "The move should be invalid.")

    def test_movement_restrictions(self):
        # Functionality 2: Movement Restrictions
        self.game.start_game(5)
        self.assertTrue(self.game.check_move((0, 0), (0, 1)), "The move should be valid.")
        self.assertFalse(self.game.check_move((0, 1), (2, 2)), "The move should be invalid.")

        self.game.start_game(4)
        self.assertTrue(self.game.check_move((0, 0), (0, 1)), "The move should be valid.")
        self.assertTrue(self.game.check_move((0, 1), (0, 2)), "The move should be valid.")
        self.assertFalse(self.game.check_move((0, 2), (0, 1)), "Revisiting a tile should be invalid.")

    def test_continuous_path_requirement(self):
        # Functionality 3: Continuous Path Requirement
        self.game.start_game(3)
        self.assertTrue(self.game.check_move((0, 0), (0, 1)), "The move should be valid.")
        self.assertFalse(self.game.check_move((0, 1), (1, 1)), "Skipping a number should be invalid.")

        self.game.start_game(4)
        self.assertTrue(self.game.check_move((0, 0), (0, 1)), "The move should be valid.")
        self.assertTrue(self.game.check_move((0, 1), (0, 2)), "The move should be valid.")
        self.assertFalse(self.game.check_move((0, 2), (1, 2)), "Skipping a number should be invalid.")

    def test_multiple_levels_with_increasing_difficulty(self):
        # Functionality 4: Multiple Levels with Increasing Difficulty
        self.game.start_game(3)
        self.assertEqual(self.game.grid.size, 3, "The grid size should be 3x3.")

        self.game.start_game(4)
        self.assertEqual(self.game.grid.size, 4, "The grid size should be 4x4.")

    def test_timer_challenge(self):
        # Functionality 5: Timer Challenge
        self.game.start_game(3)
        self.game.timer.start_timer(60)
        self.assertEqual(self.game.timer.time_remaining, 60, "The timer should start at 60 seconds.")
        self.game.timer.update_time()
        self.assertEqual(self.game.timer.time_remaining, 59, "The timer should decrement by 1 second.")

        self.game.start_game(4)
        self.game.timer.start_timer(1)
        self.game.timer.update_time()
        self.assertTrue(self.game.timer.is_time_up(), "The time should be up.")

    def test_data_storage(self):
        # Functionality 6: Data Storage
        self.game.score_manager.save_score("test_player", 200)
        scores = self.game.score_manager.get_high_scores()
        self.assertIn(("test_player", 200), scores, "The score should be saved and retrievable.")

        self.game.score_manager.load_scores('scores.txt')
        scores = self.game.score_manager.get_high_scores()
        self.assertGreaterEqual(len(scores), 1, "Scores should be loaded from the file.")

if __name__ == '__main__':
    unittest.main()
