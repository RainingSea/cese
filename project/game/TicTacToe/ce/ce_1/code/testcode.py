import unittest
import pygame
from game import Game

class TestTicTacToeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_game_initialization(self):
        # Functionality 1: Game Initialization
        self.assertEqual(self.game.board, [[' ' for _ in range(3)] for _ in range(3)], "The board should be empty at the start.")
        self.assertEqual(self.game.current_player, 'X', "Player X should start the game.")
        self.assertFalse(self.game.game_over, "The game should not be over at initialization.")

    def test_player_turn_alternation(self):
        # Functionality 2: Player Turn Alternation
        self.game.play_move(0, 0)  # Player X
        self.assertEqual(self.game.board[0][0], 'X', "Player X should place an X in the top-left cell.")
        self.assertEqual(self.game.current_player, 'O', "It should be Player O's turn next.")
        
        self.game.play_move(1, 1)  # Player O
        self.assertEqual(self.game.board[1][1], 'O', "Player O should place an O in the center cell.")
        self.assertEqual(self.game.current_player, 'X', "It should be Player X's turn next.")
        
        self.game.play_move(0, 1)  # Player X
        self.assertEqual(self.game.board[0][1], 'X', "Player X should place an X in the top-center cell.")
        self.assertEqual(self.game.current_player, 'O', "It should be Player O's turn next.")

    def test_check_winner(self):
        # Functionality 3: Check for a Winner
        self.game.play_move(0, 0)  # X
        self.game.play_move(1, 1)  # O
        self.game.play_move(0, 1)  # X
        self.game.play_move(2, 0)  # O
        self.game.play_move(0, 2)  # X
        self.assertTrue(self.game.game_over, "The game should be over when a player wins.")
        self.assertEqual(self.game.check_winner(), 'X', "Player X should be the winner.")

    def test_check_draw(self):
        # Functionality 4: Check for a Draw
        moves = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (1, 1), (2, 0), (2, 2), (2, 1)]
        players = ['X', 'O'] * 5
        for move, player in zip(moves, players):
            self.game.current_player = player
            self.game.play_move(*move)
        self.assertTrue(self.game.game_over, "The game should be over when it's a draw.")
        self.assertEqual(self.game.check_winner(), '', "There should be no winner in a draw.")

    def test_restart_game(self):
        # Functionality 5: Restart the Game
        self.game.play_move(0, 0)  # X
        self.game.restart_game()
        self.assertEqual(self.game.board, [[' ' for _ in range(3)] for _ in range(3)], "The board should be reset after restarting.")
        self.assertEqual(self.game.current_player, 'X', "Player X should start after restarting.")
        self.assertFalse(self.game.game_over, "The game should not be over after restarting.")

    def test_timer_functionality(self):
        # Functionality 6: Timer Functionality
        self.game.start_timer()
        time.sleep(1)
        elapsed_time = self.game.stop_timer()
        self.assertGreater(elapsed_time, 0, "The timer should count up correctly.")

    def test_data_storage(self):
        # Functionality 7: Data Storage
        self.game.play_move(0, 0)  # X
        self.game.play_move(1, 1)  # O
        self.game.play_move(0, 1)  # X
        self.game.play_move(2, 0)  # O
        self.game.play_move(0, 2)  # X
        with open('game_results.txt', 'r') as file:
            results = file.readlines()
        self.assertIn('Player X wins!\n', results, "The results file should contain the correct match result.")

    def test_user_feedback_at_game_end(self):
        # Functionality 8: User Feedback at Game End
        self.game.play_move(1, 1)  # X
        self.game.play_move(0, 0)  # O
        self.game.play_move(0, 1)  # X
        self.game.play_move(0, 2)  # O
        self.game.play_move(2, 0)  # X
        self.game.play_move(1, 0)  # O
        self.assertTrue(self.game.game_over, "The game should be over when Player O wins.")
        self.assertEqual(self.game.check_winner(), 'O', "Player O should be the winner.")

    def test_invalid_move_handling(self):
        # Functionality 9: Invalid Move Handling
        self.game.play_move(0, 0)  # X
        valid_move = self.game.play_move(0, 0)  # X tries to play again in the same cell
        self.assertFalse(valid_move, "The game should prevent moves in already occupied cells.")

if __name__ == '__main__':
    unittest.main()
