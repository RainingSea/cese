import unittest
import pygame
from game import Game, Board, Timer, ScoreManager

class TestNumberConnectGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.board = self.game.board
        self.timer = self.game.timer
        self.score_manager = self.game.score_manager

    def test_connect_numbers_in_sequence(self):
        # Test connecting numbers in sequence for a 3x3 grid
        self.board.initialize_grid(3)
        self.assertTrue(self.game.check_move((0, 0)), "Move to tile with number 1 should be valid")
        self.assertTrue(self.game.check_move((0, 1)), "Move to tile with number 2 should be valid")
        self.assertTrue(self.game.check_move((0, 2)), "Move to tile with number 3 should be valid")
        self.assertTrue(self.game.check_move((1, 0)), "Move to tile with number 4 should be valid")
        self.assertTrue(self.game.check_move((1, 1)), "Move to tile with number 5 should be valid")
        self.assertTrue(self.game.check_move((1, 2)), "Move to tile with number 6 should be valid")
        self.assertTrue(self.game.check_move((2, 0)), "Move to tile with number 7 should be valid")
        self.assertTrue(self.game.check_move((2, 1)), "Move to tile with number 8 should be valid")
        self.assertTrue(self.game.check_move((2, 2)), "Move to tile with number 9 should be valid")

        # Test invalid move in 4x4 grid
        self.board.initialize_grid(4)
        self.assertFalse(self.game.check_move((0, 0)), "Move to tile with number 2 should be invalid")

    def test_movement_restrictions(self):
        # Test movement restrictions in a 5x5 grid
        self.board.initialize_grid(5)
        self.assertTrue(self.game.check_move((0, 0)), "Move to tile with number 1 should be valid")
        self.assertTrue(self.game.check_move((0, 1)), "Move to tile with number 2 should be valid")
        self.assertFalse(self.game.check_move((1, 2)), "Move to tile with number 3 should be invalid")

        # Test revisiting a tile
        self.assertFalse(self.game.check_move((0, 1)), "Revisiting tile with number 2 should be invalid")

    def test_continuous_path_requirement(self):
        # Test continuous path requirement in a 3x3 grid
        self.board.initialize_grid(3)
        self.assertTrue(self.game.check_move((0, 0)), "Move to tile with number 1 should be valid")
        self.assertTrue(self.game.check_move((0, 1)), "Move to tile with number 2 should be valid")
        self.assertFalse(self.game.check_move((1, 1)), "Move to tile with number 3 should be invalid")

        # Test skipping numbers in a 4x4 grid
        self.board.initialize_grid(4)
        self.assertTrue(self.game.check_move((0, 0)), "Move to tile with number 1 should be valid")
        self.assertTrue(self.game.check_move((0, 1)), "Move to tile with number 2 should be valid")
        self.assertFalse(self.game.check_move((1, 1)), "Move to tile with number 3 should be invalid")

    def test_multiple_levels(self):
        # Test level initialization
        self.game.start_game()
        self.assertEqual(len(self.board.tiles), 3, "Level 1 should initialize with a 3x3 grid")
        self.game.start_game()
        self.assertEqual(len(self.board.tiles), 4, "Level 2 should initialize with a 4x4 grid")

    def test_timer_challenge(self):
        # Test timer functionality
        self.timer.start_timer()
        self.assertFalse(self.timer.check_time(), "Timer should not indicate time limit reached at start")
        # Simulate completing the game
        self.assertTrue(self.timer.check_time(), "Timer should indicate time limit reached after game completion")

    def test_data_storage(self):
        # Test saving score
        self.score_manager.save_score("Alice", 100)
        self.assertIn("Alice", self.score_manager.scores, "Score for Alice should be saved")
        
        # Test loading scores
        self.score_manager.load_scores()
        self.assertEqual(self.score_manager.scores["Bob"], 150, "Score for Bob should be loaded correctly")

if __name__ == '__main__':
    unittest.main()
