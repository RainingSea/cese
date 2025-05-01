import unittest
from game import Game

class TestTicTacToeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_game_initialization(self):
        # Check if the game initializes correctly
        self.assertIsNotNone(self.game.grid, "Game grid should be initialized")
        self.assertEqual(self.game.current_player.get_symbol(), 'X', "First player should be X")

    def test_player_turn_alternation(self):
        # Player X places an "X" in the top-left cell
        self.game.make_move(0, 0)
        self.assertEqual(self.game.grid.cells[0][0], 'X', "Top-left cell should be X")
        
        # Player O places an "O" in the center cell
        self.game.make_move(1, 1)
        self.assertEqual(self.game.grid.cells[1][1], 'O', "Center cell should be O")
        
        # Player X places an "X" in the top-center cell
        self.game.make_move(0, 1)
        self.assertEqual(self.game.grid.cells[0][1], 'X', "Top-center cell should be X")

    def test_check_for_winner(self):
        # Player X makes moves to win
        self.game.make_move(0, 0)  # X
        self.game.make_move(1, 1)  # O
        self.game.make_move(0, 1)  # X
        self.game.make_move(1, 0)  # O
        self.game.make_move(0, 2)  # X - X wins
        self.assertEqual(self.game.check_winner(), "X wins", "Player X should win")

    def test_check_for_draw(self):
        # Fill the grid with a draw situation
        moves = [
            (0, 0), (0, 1), (0, 2),  # X
            (1, 1), (1, 0), (1, 2),  # O
            (2, 0), (2, 1), (2, 2)   # X
        ]
        for i, (row, col) in enumerate(moves):
            self.game.make_move(row, col if i % 2 == 0 else col)
        self.assertEqual(self.game.check_winner(), "Draw", "The game should be a draw")

    def test_restart_game(self):
        # Start a game and then restart
        self.game.start_game()
        self.assertIsNone(self.game.winner, "There should be no winner at the start")
        self.game.restart_game()
        self.assertIsNone(self.game.winner, "Game should reset and have no winner")

    def test_timer_functionality(self):
        # Start a new game and check timer
        self.game.start_game()
        self.assertIsNotNone(self.game.timer.start_time, "Timer should start when the game starts")

    def test_data_storage(self):
        # Check if the results file contains the correct result (not implemented in codebase)
        self.fail("Data storage functionality is not implemented in the codebase")

    def test_user_feedback_at_game_end(self):
        # Simulate a game where Player O wins
        self.game.make_move(0, 0)  # X
        self.game.make_move(1, 1)  # O
        self.game.make_move(0, 1)  # X
        self.game.make_move(1, 0)  # O
        self.game.make_move(0, 2)  # X
        self.game.make_move(1, 2)  # O
        self.game.make_move(2, 0)  # X
        self.game.make_move(2, 1)  # O
        self.game.make_move(2, 2)  # X - X wins
        self.assertEqual(self.game.check_winner(), "X wins", "Player X should win")

    def test_invalid_move_handling(self):
        # Player X places an "X" in the top-left cell
        self.game.make_move(0, 0)
        # Attempt to place another "X" in the same cell
        self.game.make_move(0, 0)
        self.assertEqual(self.game.grid.cells[0][0], 'X', "Cell should still be X and not allow invalid move")

if __name__ == '__main__':
    unittest.main()
