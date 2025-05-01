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
        # Functionality 1: Check if the game initializes correctly
        self.assertEqual(self.game.current_player, 'X', "The first player should be X")
        self.assertEqual(self.game.grid, [['', '', ''], ['', '', ''], ['', '', '']], "The grid should be empty")

    def test_player_turn_alternation(self):
        # Functionality 2: Test player turn alternation
        self.game.make_move(0, 0)  # Player X
        self.assertEqual(self.game.current_player, 'O', "Current player should be O after X's turn")
        self.game.make_move(1, 1)  # Player O
        self.assertEqual(self.game.current_player, 'X', "Current player should be X after O's turn")
        self.game.make_move(0, 1)  # Player X
        self.assertEqual(self.game.current_player, 'O', "Current player should be O after X's turn")

    def test_check_winner(self):
        # Functionality 3: Test winner detection
        self.game.make_move(0, 0)  # X
        self.game.make_move(1, 1)  # O
        self.game.make_move(0, 1)  # X
        self.game.make_move(1, 0)  # O
        self.game.make_move(0, 2)  # X
        winner = self.game.check_winner()
        self.assertEqual(winner, 'Player X wins!', "The winner should be Player X")

    def test_check_draw(self):
        # Functionality 4: Test draw detection
        moves = [
            (0, 0), (0, 1), (0, 2),
            (1, 1), (1, 0), (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]
        for i, (x, y) in enumerate(moves):
            self.game.make_move(x, y if i % 2 == 0 else y)  # Alternate between X and O
        winner = self.game.check_winner()
        self.assertEqual(winner, 'Draw!', "The game should end in a draw")

    def test_restart_game(self):
        # Functionality 5: Test game restart
        self.game.make_move(0, 0)  # X
        self.game.make_move(1, 1)  # O
        self.game.reset_game()
        self.assertEqual(self.game.current_player, 'X', "After reset, the current player should be X")
        self.assertEqual(self.game.grid, [['', '', ''], ['', '', ''], ['', '', '']], "The grid should be empty after reset")

    def test_timer_functionality(self):
        # Functionality 6: Test timer functionality
        self.game.start_game()
        time_before_move = self.game.timer
        self.game.make_move(0, 0)  # X
        self.assertGreater(self.game.timer, time_before_move, "Timer should increase after a move")

    def test_data_storage(self):
        # Functionality 7: Test data storage
        self.game.make_move(0, 0)  # X
        self.game.make_move(1, 1)  # O
        self.game.make_move(0, 1)  # X
        self.game.make_move(1, 0)  # O
        self.game.make_move(0, 2)  # X
        self.assertTrue(os.path.exists('game_results.txt'), "Results file should exist after game ends")
        with open('game_results.txt', 'r') as file:
            results = file.readlines()
        self.assertIn('Player X wins!', results[-1], "The results file should contain the correct game outcome")

    def test_user_feedback_at_game_end(self):
        # Functionality 8: Test user feedback at game end
        self.game.make_move(0, 0)  # X
        self.game.make_move(1, 1)  # O
        self.game.make_move(0, 1)  # X
        self.game.make_move(1, 0)  # O
        self.game.make_move(0, 2)  # X
        winner = self.game.check_winner()
        self.assertEqual(winner, 'Player X wins!', "Feedback should indicate Player X wins")

    def test_invalid_move_handling(self):
        # Functionality 9: Test invalid move handling
        self.game.make_move(0, 0)  # X
        self.game.make_move(0, 0)  # Invalid move
        self.assertEqual(self.game.grid[0][0], 'X', "The cell should still contain X after an invalid move")

if __name__ == '__main__':
    unittest.main()
