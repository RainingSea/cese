import unittest
import pygame
from game import Game
from player import Player

class TestGomokuGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_initialize_game_board(self):
        # Functionalities 1: Initialize the Game Board
        expected_board_size = 15
        self.assertEqual(len(self.game.board), expected_board_size, "Board should have 15 rows")
        self.assertEqual(len(self.game.board[0]), expected_board_size, "Board should have 15 columns")
        for row in self.game.board:
            for cell in row:
                self.assertIsNone(cell, "All cells should be initialized to None")

    def test_assign_player_colors(self):
        # Functionalities 2: Assign Player Colors
        self.assertEqual(self.game.players['Black'].color, 'black', "Player one should have black pieces")
        self.assertEqual(self.game.players['White'].color, 'white', "Player two should have white pieces")

    def test_place_piece_on_board(self):
        # Functionalities 3: Place a Piece on the Board
        x, y = 40, 40  # Coordinates for the first cell
        self.assertTrue(self.game.place_piece(x, y), "Piece should be placed successfully")
        self.assertEqual(self.game.board[1][1], 'Black', "The piece should be black")
        self.assertEqual(self.game.current_player, 'White', "Next player should be White")

    def test_check_for_victory(self):
        # Functionalities 4: Check for Victory
        # Simulate a winning condition
        for i in range(5):
            self.game.board[0][i] = 'Black'
        self.assertTrue(self.game.check_victory(), "There should be a victory condition")
        self.assertEqual(self.game.winner, 'Black', "Black should be the winner")

    def test_display_winning_player_information(self):
        # Functionalities 5: Display Winning Player Information
        # This functionality is not implemented in the codebase
        self.fail("Display winning player information functionality is not implemented in the codebase")

    def test_prevent_further_moves_after_victory(self):
        # Functionalities 6: Prevent Further Moves After Victory
        # Simulate a winning condition
        for i in range(5):
            self.game.board[0][i] = 'Black'
        self.game.check_victory()
        self.assertFalse(self.game.place_piece(80, 80), "No further moves should be allowed after victory")

    def test_save_game_state_to_file(self):
        # Functionalities 7: Save Game State to a File
        self.game.save_game_state()
        with open('game_data.txt', 'r') as f:
            data = f.read()
        self.assertIn('"current_player": "Black"', data, "Game state should be saved with current player")

    def test_load_game_state_from_file(self):
        # Functionalities 8: Load Game State from a File
        self.game.save_game_state()
        self.game.board[0][0] = 'White'
        self.game.load_game_state()
        self.assertIsNone(self.game.board[0][0], "Game state should be loaded correctly from file")

    def test_validate_input_for_piece_placement(self):
        # Functionalities 9: Validate Input for Piece Placement
        x, y = 40, 40  # Coordinates for the first cell
        self.game.place_piece(x, y)
        self.assertFalse(self.game.place_piece(x, y), "Should not allow placing on a non-empty square")
        self.assertFalse(self.game.place_piece(-10, -10), "Should not allow placing out of bounds")

if __name__ == '__main__':
    unittest.main()
