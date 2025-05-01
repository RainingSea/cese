import unittest
import pygame
import os
from game import Game

class TestTicTacToeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()
        self.game.start_game()

    def test_game_initialization(self):
        # Functionality 1: Game Initialization
        self.assertEqual(self.game.current_turn, 'X', "The first player should be X")
        self.assertEqual(self.game.board, [['', '', ''], ['', '', ''], ['', '', '']], "The game board should be empty")

    def test_player_turn_alternation(self):
        # Functionality 2: Player Turn Alternation
        self.game.make_move(0, 0)  # X
        self.assertEqual(self.game.board[0][0], 'X', "X should be placed in the top-left cell")
        self.assertEqual(self.game.current_turn, 'O', "Next turn should be O")

        self.game.make_move(1, 1)  # O
        self.assertEqual(self.game.board[1][1], 'O', "O should be placed in the center cell")
        self.assertEqual(self.game.current_turn, 'X', "Next turn should be X")

        self.game.make_move(0, 1)  # X
        self.assertEqual(self.game.board[0][1], 'X', "X should be placed in the top-center cell")
        self.assertEqual(self.game.current_turn, 'O', "Next turn should be O")

    def test_check_for_winner(self):
        # Functionality 3: Check for a Winner
        self.game.make_move(0, 0)  # X
        self.game.make_move(1, 1)  # O
        self.game.make_move(0, 1)  # X
        self.game.make_move(1, 0)  # O
        self.game.make_move(0, 2)  # X
        winner = self.game.check_winner()
        self.assertEqual(winner, 'X', "Player X should be the winner")

    def test_check_for_draw(self):
        # Functionality 4: Check for a Draw
        moves = [
            (0, 0), (0, 1), (1, 1), (0, 2),
            (1, 0), (1, 2), (2, 0), (2, 1),
            (2, 2)
        ]
        for i, (x, y) in enumerate(moves):
            self.game.make_move(x, y if i % 2 == 0 else y)  # Alternate X and O
        winner = self.game.check_winner()
        self.assertEqual(winner, 'Draw', "The game should end in a draw")

    def test_restart_game(self):
        # Functionality 5: Restart the Game
        self.game.make_move(0, 0)  # X
        self.game.restart_game()
        self.assertEqual(self.game.current_turn, 'X', "After restart, the first player should be X")
        self.assertEqual(self.game.board, [['', '', ''], ['', '', ''], ['', '', '']], "The game board should be empty after restart")

    def test_timer_functionality(self):
        # Functionality 6: Timer Functionality
        self.game.start_time = 0  # Simulate starting time
        self.game.timer = int(time.time() - self.game.start_time)
        self.assertGreaterEqual(self.game.timer, 0, "Timer should count up correctly")

    def test_data_storage(self):
        # Functionality 7: Data Storage
        self.game.save_result('X', 30)
        with open('results.txt', 'r') as f:
            results = f.readlines()
        self.assertIn('X|30\n', results, "Results file should contain the correct match result")

    def test_user_feedback_at_game_end(self):
        # Functionality 8: User Feedback at Game End
        self.game.make_move(0, 0)  # X
        self.game.make_move(1, 1)  # O
        self.game.make_move(0, 1)  # X
        self.game.make_move(1, 0)  # O
        self.game.make_move(0, 2)  # X
        winner = self.game.check_winner()
        self.assertEqual(winner, 'X', "Player X should be the winner")

    def test_invalid_move_handling(self):
        # Functionality 9: Invalid Move Handling
        self.game.make_move(0, 0)  # X
        self.game.make_move(0, 0)  # Invalid move
        self.assertEqual(self.game.board[0][0], 'X', "Cell should not be overwritten")

if __name__ == '__main__':
    unittest.main()
