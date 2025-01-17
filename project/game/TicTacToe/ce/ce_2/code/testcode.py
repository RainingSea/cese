import unittest
import pygame
from game import Game

class TestTicTacToeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_game_initialization(self):
        # Functionality 1: Game Initialization
        self.assertEqual(self.game.current_player, "X", "The first player should be X")
        self.assertEqual(self.game.board, [["", "", ""], ["", "", ""], ["", "", ""]], "The board should be empty at the start")

    def test_player_turn_alternation(self):
        # Functionality 2: Player Turn Alternation
        self.game.play_move(0, 0)  # X
        self.assertEqual(self.game.current_player, "O", "After X plays, it should be O's turn")
        self.game.play_move(1, 1)  # O
        self.assertEqual(self.game.current_player, "X", "After O plays, it should be X's turn")
        self.game.play_move(0, 1)  # X
        self.assertEqual(self.game.current_player, "O", "After X plays, it should be O's turn")

    def test_check_winner(self):
        # Functionality 3: Check for a Winner
        self.game.play_move(0, 0)  # X
        self.game.play_move(1, 1)  # O
        self.game.play_move(0, 1)  # X
        self.game.play_move(2, 0)  # O
        result = self.game.play_move(0, 2)  # X
        self.assertEqual(result, "X wins!", "Player X should win with a horizontal line at the top")

    def test_check_draw(self):
        # Functionality 4: Check for a Draw
        moves = [(0, 0), (0, 1), (1, 1), (2, 2), (0, 2), (2, 0), (1, 0), (1, 2), (2, 1)]
        players = ["X", "O"] * 5
        for move, player in zip(moves, players):
            self.game.play_move(*move)
        result = self.game.check_winner()
        self.assertEqual(result, "It's a draw!", "The game should end in a draw")

    def test_restart_game(self):
        # Functionality 5: Restart the Game
        self.game.play_move(0, 0)  # X
        self.game.reset_game()
        self.assertEqual(self.game.current_player, "X", "The first player should be X after reset")
        self.assertEqual(self.game.board, [["", "", ""], ["", "", ""], ["", "", ""]], "The board should be empty after reset")

    def test_timer_functionality(self):
        # Functionality 6: Timer Functionality
        self.game.start_timer()
        time.sleep(1)
        elapsed_time = self.game.stop_timer()
        self.assertGreater(elapsed_time, 0, "The timer should count up correctly")

    def test_data_storage(self):
        # Functionality 7: Data Storage
        self.game.play_move(0, 0)  # X
        self.game.save_game_data()
        self.game.reset_game()
        self.game.load_game_data()
        self.assertEqual(self.game.board[0][0], "X", "The game data should be loaded correctly")
        self.assertEqual(self.game.current_player, "O", "The current player should be O after loading data")

    def test_user_feedback_at_game_end(self):
        # Functionality 8: User Feedback at Game End
        self.game.play_move(0, 0)  # X
        self.game.play_move(1, 1)  # O
        self.game.play_move(0, 1)  # X
        self.game.play_move(2, 0)  # O
        result = self.game.play_move(0, 2)  # X
        self.assertEqual(result, "X wins!", "A message should indicate Player X has won")

    def test_invalid_move_handling(self):
        # Functionality 9: Invalid Move Handling
        self.game.play_move(0, 0)  # X
        result = self.game.play_move(0, 0)  # X tries again
        self.assertEqual(result, "Invalid move", "The game should prevent placing a symbol in an occupied cell")

if __name__ == '__main__':
    unittest.main()
