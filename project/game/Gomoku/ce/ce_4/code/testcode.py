import unittest
from game import Game

class TestGomokuGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_initialize_game_board(self):
        # Functionalities 1: Initialize the Game Board
        self.assertEqual(len(self.game.board), 15, "The board should have 15 rows")
        self.assertEqual(len(self.game.board[0]), 15, "The board should have 15 columns")
        for row in self.game.board:
            for cell in row:
                self.assertEqual(cell, '', "Each cell should be initialized as empty")

    def test_assign_player_colors(self):
        # Functionalities 2: Assign Player Colors
        self.assertEqual(self.game.current_player, 'Black', "Player one should be assigned black pieces")

    def test_place_piece_on_board(self):
        # Functionalities 3: Place a Piece on the Board
        self.assertTrue(self.game.place_piece(0, 0), "Should be able to place a piece on an empty square")
        self.assertEqual(self.game.board[0][0], 'Black', "The piece should be marked as black")
        self.assertFalse(self.game.place_piece(0, 0), "Should not be able to place a piece on a non-empty square")

    def test_check_victory(self):
        # Functionalities 4: Check for Victory
        for i in range(5):
            self.game.place_piece(i, 0)
        self.assertTrue(self.game.check_victory(), "Should detect a victory when five pieces are aligned")
        self.assertEqual(self.game.winner, 'Black', "The winner should be the current player")

    def test_display_winning_player_information(self):
        # Functionalities 5: Display Winning Player Information
        for i in range(5):
            self.game.place_piece(i, 0)
        self.game.check_victory()
        with self.assertLogs() as log:
            self.game.display_winner()
            self.assertIn("The winner is: Black", log.output[0], "The winning player's information should be displayed")

    def test_prevent_further_moves_after_victory(self):
        # Functionalities 6: Prevent Further Moves After Victory
        for i in range(5):
            self.game.place_piece(i, 0)
        self.game.check_victory()
        self.assertFalse(self.game.place_piece(5, 0), "Should not allow placing a piece after a victory")

    def test_save_game_state_to_file(self):
        # Functionalities 7: Save Game State to a File
        self.game.winner = 'Black'
        self.game.save_results()
        with open('game_results.txt', 'r') as f:
            lines = f.readlines()
            self.assertIn('Black\n', lines, "The game state should be saved to the file")

    def test_load_game_state_from_file(self):
        # Functionalities 8: Load Game State from a File (not implemented in codebase)
        self.fail("Load game state functionality is not implemented in the codebase")

    def test_validate_input_for_piece_placement(self):
        # Functionalities 9: Validate Input for Piece Placement
        self.assertFalse(self.game.place_piece(15, 15), "Should not allow placing a piece out of bounds")
        self.game.place_piece(0, 0)
        self.assertFalse(self.game.place_piece(0, 0), "Should not allow placing a piece on a non-empty square")

if __name__ == '__main__':
    unittest.main()
