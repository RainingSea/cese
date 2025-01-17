import unittest
import json
from game import Game

class TestGomokuGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_initialize_game_board(self):
        # Functionalities 1: Initialize the Game Board
        expected_board = [['' for _ in range(15)] for _ in range(15)]
        self.assertEqual(self.game.board, expected_board, "Game board should be initialized with empty squares")

    def test_assign_player_colors(self):
        # Functionalities 2: Assign Player Colors
        self.assertEqual(self.game.current_turn, 'black', "Player one should start with black pieces")

    def test_place_piece_on_board(self):
        # Functionalities 3: Place a Piece on the Board
        self.assertTrue(self.game.place_piece(0, 0), "Should be able to place a piece on an empty square")
        self.assertEqual(self.game.board[0][0], 'black', "The square should be marked with a black piece")
        self.assertEqual(self.game.current_turn, 'white', "Turn should switch to white after a move")

    def test_check_for_victory(self):
        # Functionalities 4: Check for Victory
        for i in range(5):
            self.game.place_piece(i, 0)
            self.game.place_piece(i, 1)  # Alternate moves to simulate turns
        self.assertTrue(self.game.check_victory(), "Should detect a victory when five pieces are aligned")

    def test_display_winning_player_information(self):
        # Functionalities 5: Display Winning Player Information
        # This functionality is not implemented in the codebase
        self.fail("Display winning player information is not implemented in the codebase")

    def test_prevent_further_moves_after_victory(self):
        # Functionalities 6: Prevent Further Moves After Victory
        for i in range(5):
            self.game.place_piece(i, 0)
            self.game.place_piece(i, 1)  # Alternate moves to simulate turns
        self.assertTrue(self.game.check_victory(), "Should detect a victory")
        self.assertFalse(self.game.place_piece(5, 0), "Should not allow moves after a victory")

    def test_save_game_state_to_file(self):
        # Functionalities 7: Save Game State to a File
        self.game.place_piece(0, 0)
        self.game.save_game_state()
        with open('game_state.txt', 'r') as f:
            state = json.load(f)
        self.assertEqual(state['board'][0][0], 'black', "Game state should be saved with the current board state")
        self.assertEqual(state['current_turn'], 'white', "Game state should save the current player's turn")

    def test_load_game_state_from_file(self):
        # Functionalities 8: Load Game State from a File
        self.game.place_piece(0, 0)
        self.game.save_game_state()
        new_game = Game()
        new_game.load_game_state()
        self.assertEqual(new_game.board[0][0], 'black', "Loaded game state should reflect saved board state")
        self.assertEqual(new_game.current_turn, 'white', "Loaded game state should reflect saved player's turn")

    def test_validate_input_for_piece_placement(self):
        # Functionalities 9: Validate Input for Piece Placement
        self.game.place_piece(0, 0)
        self.assertFalse(self.game.place_piece(0, 0), "Should not allow placing a piece on a non-empty square")
        self.assertFalse(self.game.place_piece(15, 15), "Should not allow placing a piece out of bounds")

if __name__ == '__main__':
    unittest.main()
