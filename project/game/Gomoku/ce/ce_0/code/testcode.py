import unittest
import json
import os
from game import Game

class TestGomokuGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_initialize_game_board(self):
        # Functionalities 1: Initialize the Game Board
        expected_board = [['' for _ in range(15)] for _ in range(15)]
        self.assertEqual(self.game.board, expected_board, "The game board should be initialized correctly.")

    def test_assign_player_colors(self):
        # Functionalities 2: Assign Player Colors
        self.assertEqual(self.game.current_player, 'black', "Player one should have black pieces.")
        self.game.place_piece(0, 0)  # Simulate a move to change the player
        self.assertEqual(self.game.current_player, 'white', "Player two should have white pieces.")

    def test_place_piece_on_board(self):
        # Functionalities 3: Place a Piece on the Board
        self.assertTrue(self.game.place_piece(0, 0), "Should be able to place a piece on an empty square.")
        self.assertEqual(self.game.board[0][0], 'black', "The square should be marked with a black piece.")

    def test_check_for_victory(self):
        # Functionalities 4: Check for Victory
        for i in range(5):
            self.game.place_piece(i, 0)
            if i < 4:
                self.assertIsNone(self.game.winner, "There should be no winner yet.")
        self.assertEqual(self.game.winner, 'black', "Black should be the winner after aligning five pieces.")

    def test_display_winning_player_information(self):
        # Functionalities 5: Display Winning Player Information
        for i in range(5):
            self.game.place_piece(i, 0)
        self.assertEqual(self.game.winner, 'black', "The winning player should be black.")

    def test_prevent_further_moves_after_victory(self):
        # Functionalities 6: Prevent Further Moves After Victory
        for i in range(5):
            self.game.place_piece(i, 0)
        self.assertFalse(self.game.place_piece(5, 0), "No further moves should be allowed after a victory.")

    def test_save_game_state_to_file(self):
        # Functionalities 7: Save Game State to a File
        self.game.save_game()
        self.assertTrue(os.path.exists('game_data.txt'), "The game state should be saved to a file.")

    def test_load_game_state_from_file(self):
        # Functionalities 8: Load Game State from a File
        self.game.save_game()
        new_game = Game()
        new_game.load_game()
        self.assertEqual(new_game.board, self.game.board, "The loaded game board should match the saved state.")
        self.assertEqual(new_game.current_player, self.game.current_player, "The loaded current player should match the saved state.")

    def test_validate_input_for_piece_placement(self):
        # Functionalities 9: Validate Input for Piece Placement
        self.game.place_piece(0, 0)
        self.assertFalse(self.game.place_piece(0, 0), "Should not be able to place a piece on a non-empty square.")
        self.assertFalse(self.game.place_piece(15, 15), "Should not be able to place a piece out of bounds.")

if __name__ == '__main__':
    unittest.main()
