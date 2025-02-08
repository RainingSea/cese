import unittest
import pygame
from game import Game

class TestGomokuGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_initialize_game_board(self):
        # Functionalities 1: Initialize the Game Board
        self.assertEqual(len(self.game.board), 15, "Board should have 15 rows")
        self.assertEqual(len(self.game.board[0]), 15, "Board should have 15 columns")
        for row in self.game.board:
            for cell in row:
                self.assertEqual(cell, '', "Each cell should be initialized as empty")

    def test_assign_player_colors(self):
        # Functionalities 2: Assign Player Colors
        player1 = Player("Player 1", "black")
        player2 = Player("Player 2", "white")
        self.assertEqual(player1.color, "black", "Player 1 should have black pieces")
        self.assertEqual(player2.color, "white", "Player 2 should have white pieces")

    def test_place_piece_on_board(self):
        # Functionalities 3: Place a Piece on the Board
        self.assertTrue(self.game.place_piece(0, 0), "Should be able to place a piece on an empty square")
        self.assertEqual(self.game.board[0][0], 'black', "The piece should be black")
        self.assertFalse(self.game.place_piece(0, 0), "Should not be able to place a piece on a non-empty square")

    def test_check_for_victory(self):
        # Functionalities 4: Check for Victory
        for i in range(5):
            self.game.place_piece(i, 0)
        self.assertTrue(self.game.check_victory(), "Should detect victory when 5 pieces are aligned")
        self.assertEqual(self.game.winner, 'black', "The winner should be black")

    def test_display_winning_player_information(self):
        # Functionalities 5: Display Winning Player Information
        self.game.winner = 'black'
        screen = pygame.Surface((600, 600))
        self.game.display_winner(screen)
        # Since we cannot directly test the display, we assume the method works if no errors occur

    def test_prevent_further_moves_after_victory(self):
        # Functionalities 6: Prevent Further Moves After Victory
        for i in range(5):
            self.game.place_piece(i, 0)
        self.assertTrue(self.game.check_victory(), "Should detect victory")
        self.assertFalse(self.game.place_piece(5, 0), "Should not allow moves after victory")

    def test_save_game_state_to_file(self):
        # Functionalities 7: Save Game State to a File
        self.game.save_game_state()
        with open('game_state.txt', 'r') as f:
            state = json.load(f)
        self.assertEqual(state['current_turn'], self.game.current_turn, "Current turn should match saved state")
        self.assertEqual(state['winner'], self.game.winner, "Winner should match saved state")

    def test_load_game_state_from_file(self):
        # Functionalities 8: Load Game State from a File
        self.game.board[0][0] = 'black'
        self.game.save_game_state()
        self.game.board[0][0] = ''
        self.game.load_game_state()
        self.assertEqual(self.game.board[0][0], 'black', "Board should reflect loaded state")

    def test_validate_input_for_piece_placement(self):
        # Functionalities 9: Validate Input for Piece Placement
        self.assertFalse(self.game.place_piece(15, 15), "Should not allow placing a piece out of bounds")
        self.game.place_piece(0, 0)
        self.assertFalse(self.game.place_piece(0, 0), "Should not allow placing a piece on a non-empty square")

if __name__ == '__main__':
    unittest.main()
