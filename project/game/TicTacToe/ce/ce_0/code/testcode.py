import unittest
import pygame
from game import Game
from ui import UI

class TestTicTacToeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and UI components
        self.game = Game()
        self.ui = UI(self.game)

    def test_game_initialization(self):
        # Functionality 1: Game Initialization
        self.assertEqual(self.game.current_turn, 'X', "Initial turn should be Player X")
        self.assertEqual(self.game.board, [['', '', ''], ['', '', ''], ['', '', '']], "Initial board should be empty")

    def test_player_turn_alternation(self):
        # Functionality 2: Player Turn Alternation
        self.game.play_move(0, 0)  # X
        self.assertEqual(self.game.board[0][0], 'X', "Player X should place X in top-left cell")
        self.assertEqual(self.game.current_turn, 'O', "Next turn should be Player O")

        self.game.play_move(1, 1)  # O
        self.assertEqual(self.game.board[1][1], 'O', "Player O should place O in center cell")
        self.assertEqual(self.game.current_turn, 'X', "Next turn should be Player X")

        self.game.play_move(0, 1)  # X
        self.assertEqual(self.game.board[0][1], 'X', "Player X should place X in top-center cell")
        self.assertEqual(self.game.current_turn, 'O', "Next turn should be Player O")

    def test_check_winner(self):
        # Functionality 3: Check for a Winner
        self.game.play_move(0, 0)  # X
        self.game.play_move(1, 1)  # O
        self.game.play_move(0, 1)  # X
        self.game.play_move(2, 0)  # O
        self.game.play_move(0, 2)  # X
        winner = self.game.check_winner()
        self.assertEqual(winner, 'X', "Player X should win with a horizontal line at the top")

    def test_check_draw(self):
        # Functionality 4: Check for a Draw
        moves = [(0, 0), (0, 1), (1, 1), (1, 0), (2, 2), (0, 2), (2, 0), (1, 2), (2, 1)]
        for move in moves:
            self.game.play_move(*move)
        result = self.game.check_winner()
        self.assertEqual(result, 'Draw', "The game should end in a draw")

    def test_restart_game(self):
        # Functionality 5: Restart the Game
        self.game.play_move(0, 0)  # X
        self.game.reset_game()
        self.assertEqual(self.game.current_turn, 'X', "After reset, the first turn should be Player X")
        self.assertEqual(self.game.board, [['', '', ''], ['', '', ''], ['', '', '']], "Board should be empty after reset")

    def test_timer_functionality(self):
        # Functionality 6: Timer Functionality
        self.game.start_timer()
        time.sleep(1)
        self.game.stop_timer()
        self.assertGreater(self.game.timer, 0, "Timer should count up correctly")

    def test_data_storage(self):
        # Functionality 7: Data Storage (not implemented in codebase)
        self.fail("Data storage functionality is not implemented in the codebase")

    def test_user_feedback_at_game_end(self):
        # Functionality 8: User Feedback at Game End (not implemented in codebase)
        self.fail("User feedback at game end is not implemented in the codebase")

    def test_invalid_move_handling(self):
        # Functionality 9: Invalid Move Handling
        self.game.play_move(0, 0)  # X
        valid_move = self.game.play_move(0, 0)  # Attempt to place X again in the same cell
        self.assertFalse(valid_move, "The game should prevent placing a symbol in an occupied cell")

if __name__ == '__main__':
    unittest.main()
