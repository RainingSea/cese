import unittest
from game import Game

class TestTicTacToeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_game_initialization(self):
        # Functionality 1: Game Initialization
        self.assertEqual(self.game.current_player, "X", "First player should be X")
        self.assertEqual(self.game.board, [["", "", ""], ["", "", ""], ["", "", ""]], "Board should be empty initially")

    def test_player_turn_alternation(self):
        # Functionality 2: Player Turn Alternation
        self.game.play_move(0, 0)  # X
        self.assertEqual(self.game.board[0][0], "X", "Player X should place an X in the top-left cell")
        self.assertEqual(self.game.current_player, "O", "Next player should be O")

        self.game.play_move(1, 1)  # O
        self.assertEqual(self.game.board[1][1], "O", "Player O should place an O in the center cell")
        self.assertEqual(self.game.current_player, "X", "Next player should be X")

        self.game.play_move(0, 1)  # X
        self.assertEqual(self.game.board[0][1], "X", "Player X should place an X in the top-center cell")
        self.assertEqual(self.game.current_player, "O", "Next player should be O")

    def test_check_for_winner(self):
        # Functionality 3: Check for a Winner
        self.game.play_move(0, 0)  # X
        self.game.play_move(1, 1)  # O
        self.game.play_move(0, 1)  # X
        self.game.play_move(2, 0)  # O
        self.game.play_move(0, 2)  # X
        self.assertEqual(self.game.winner, "X", "Player X should win with a horizontal line at the top")

    def test_check_for_draw(self):
        # Functionality 4: Check for a Draw
        moves = [(0, 0), (0, 1), (1, 1), (2, 2), (0, 2), (2, 0), (1, 0), (1, 2), (2, 1)]
        players = ["X", "O"] * 5
        for move, player in zip(moves, players):
            self.game.play_move(*move)
        self.assertTrue(self.game.is_draw, "The game should be a draw")
        self.assertIsNone(self.game.winner, "There should be no winner in a draw")

    def test_restart_game(self):
        # Functionality 5: Restart the Game
        self.game.play_move(0, 0)  # X
        self.game.restart_game()
        self.assertEqual(self.game.board, [["", "", ""], ["", "", ""], ["", "", ""]], "Board should be reset")
        self.assertEqual(self.game.current_player, "X", "First player should be X after restart")

    def test_timer_functionality(self):
        # Functionality 6: Timer Functionality
        self.game.play_move(0, 0)  # X
        self.game.play_move(1, 1)  # O
        self.assertGreater(self.game.get_duration(), 0, "Timer should count up correctly")

    def test_data_storage(self):
        # Functionality 7: Data Storage
        self.game.play_move(0, 0)  # X
        self.game.play_move(1, 1)  # O
        self.game.play_move(0, 1)  # X
        self.game.play_move(2, 0)  # O
        self.game.play_move(0, 2)  # X
        self.game.save_result()
        with open("game_results.txt", "r") as file:
            results = file.readlines()
        self.assertIn("Winner: X", results[-1], "The result should be saved with Player X as the winner")

    def test_user_feedback_at_game_end(self):
        # Functionality 8: User Feedback at Game End
        self.fail("User feedback at game end functionality is not implemented in the codebase")

    def test_invalid_move_handling(self):
        # Functionality 9: Invalid Move Handling
        self.game.play_move(0, 0)  # X
        self.game.play_move(0, 0)  # Invalid move by O
        self.assertEqual(self.game.board[0][0], "X", "The cell should remain occupied by X")
        self.assertEqual(self.game.current_player, "O", "Player O should still be the current player after an invalid move")

if __name__ == '__main__':
    unittest.main()
