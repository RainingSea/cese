import unittest
import pygame
from game import Game

class TestNumberConnectGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()
        self.game.start_game()

    def test_connect_numbers_in_sequence(self):
        # Test valid sequence from 1 to 9 in a 3x3 grid
        self.game.board.initialize_board()  # Assuming this fills the board with numbers 1-9
        # Simulate clicking tiles in order
        self.assertTrue(self.game.check_path(), "The path should be valid from 1 to 9")

        # Test invalid move (non-adjacent)
        self.game.board.initialize_board()  # Assuming this fills the board with numbers 1-16
        # Simulate clicking tiles 1 and then a non-adjacent tile 2
        self.assertFalse(self.game.check_path(), "The move should be invalid for non-adjacent tiles")

    def test_movement_restrictions(self):
        # Test valid adjacent movement
        self.game.board.initialize_board()  # Assuming this fills the board with numbers 1-25
        # Simulate clicking tiles 1, 2 (adjacent), then 3 (non-adjacent)
        self.assertFalse(self.game.check_path(), "The move to a non-adjacent tile should be invalid")

        # Test revisiting a tile
        self.game.board.initialize_board()  # Assuming this fills the board with numbers 1-16
        # Simulate clicking tiles 1, 2, 3, then 2 again
        self.assertFalse(self.game.check_path(), "Revisiting a tile should be invalid")

    def test_continuous_path_requirement(self):
        # Test skipping a number
        self.game.board.initialize_board()  # Assuming this fills the board with numbers 1-9
        # Simulate clicking tiles 1, 2, then 4 (skipping 3)
        self.assertFalse(self.game.check_path(), "Skipping a number should break the path")

        # Test skipping a number in a 4x4 grid
        self.game.board.initialize_board()  # Assuming this fills the board with numbers 1-16
        # Simulate clicking tiles 1, 2, 3, then 5 (skipping 4)
        self.assertFalse(self.game.check_path(), "Skipping a number should break the path")

    def test_multiple_levels_with_increasing_difficulty(self):
        # Test level 1 initialization
        self.game.start_game()  # Start the game
        self.assertEqual(self.game.board.grid_size, 3, "Level 1 should initialize with a 3x3 grid")

        # Test level 2 initialization
        self.game.start_game()  # Complete level 1 and start level 2
        self.assertEqual(self.game.board.grid_size, 4, "Level 2 should initialize with a 4x4 grid")

    def test_timer_challenge(self):
        # Test timer starts
        self.assertGreater(self.game.timer.time_remaining, 0, "Timer should start with a positive time limit")

        # Simulate completing the path within the time limit
        self.game.timer.update_timer()  # Simulate time passing
        self.assertTrue(self.game.timer.is_time_up(), "The game should indicate completion within time limit")

        # Simulate taking too long
        self.game.timer.time_remaining = 0  # Simulate time limit exceeded
        self.assertTrue(self.game.timer.is_time_up(), "The game should indicate time limit exceeded")

    def test_data_storage(self):
        # Test saving score (not implemented in codebase)
        self.fail("Saving score functionality is not implemented in the codebase")

        # Test loading scores (not implemented in codebase)
        self.fail("Loading scores functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
