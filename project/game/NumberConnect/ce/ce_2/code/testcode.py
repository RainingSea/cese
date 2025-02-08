import unittest
from game import Game, Grid, Timer

class TestNumberConnectGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()

    def test_connect_numbers_in_sequence(self):
        # Functionality 1: Connect Numbers in Sequence
        # Test case 1: Valid sequence in a 3x3 grid
        self.game.grid = Grid(size=3)
        path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0), (1, 1)]
        self.assertTrue(self.game.check_path(path), "The path should be valid for a correct sequence.")

        # Test case 2: Invalid move with non-adjacent tiles in a 4x4 grid
        self.game.grid = Grid(size=4)
        path = [(0, 0), (2, 2)]
        self.assertFalse(self.game.check_path(path), "The path should be invalid for non-adjacent tiles.")

    def test_movement_restrictions(self):
        # Functionality 2: Movement Restrictions
        # Test case 1: Non-adjacent move in a 5x5 grid
        self.game.grid = Grid(size=5)
        path = [(0, 0), (0, 1), (2, 2)]
        self.assertFalse(self.game.check_path(path), "The path should be invalid for non-adjacent move.")

        # Test case 2: Revisiting a tile in a 4x4 grid
        self.game.grid = Grid(size=4)
        path = [(0, 0), (0, 1), (0, 2), (0, 1)]
        self.assertFalse(self.game.check_path(path), "The path should be invalid for revisiting a tile.")

    def test_continuous_path_requirement(self):
        # Functionality 3: Continuous Path Requirement
        # Test case 1: Skipping a number in a 3x3 grid
        self.game.grid = Grid(size=3)
        path = [(0, 0), (0, 1), (1, 1)]
        self.assertFalse(self.game.check_path(path), "The path should be invalid for skipping a number.")

        # Test case 2: Skipping a number in a 4x4 grid
        self.game.grid = Grid(size=4)
        path = [(0, 0), (0, 1), (0, 2), (1, 2)]
        self.assertFalse(self.game.check_path(path), "The path should be invalid for skipping a number.")

    def test_multiple_levels_with_increasing_difficulty(self):
        # Functionality 4: Multiple Levels with Increasing Difficulty
        # Test case 1: Initialize level 1 with a 3x3 grid
        self.game.start_game(level=1)
        self.assertEqual(len(self.game.grid.tiles), 3, "Level 1 should initialize with a 3x3 grid.")

        # Test case 2: Initialize level 2 with a 4x4 grid
        self.game.start_game(level=2)
        self.assertEqual(len(self.game.grid.tiles), 4, "Level 2 should initialize with a 4x4 grid.")

    def test_timer_challenge(self):
        # Functionality 5: Timer Challenge
        # Test case 1: Timer starts with a 3x3 grid
        self.game.start_game(level=1)
        self.assertEqual(self.game.timer.time_remaining, 60, "Timer should start with 60 seconds.")

        # Test case 2: Timer expiration
        self.game.timer.start_timer(1)
        self.game.update_timer()
        self.assertTrue(self.game.timer.is_time_up(), "Timer should indicate time up after expiration.")

    def test_data_storage(self):
        # Functionality 6: Data Storage
        # Test case 1: Save score functionality (not implemented in codebase)
        self.fail("Save score functionality is not implemented in the codebase.")

        # Test case 2: Load score functionality (not implemented in codebase)
        self.fail("Load score functionality is not implemented in the codebase.")

if __name__ == '__main__':
    unittest.main()
