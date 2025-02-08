import unittest
from game import Game

class TestTicTacToeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_game_initialization(self):
        # Functionality 1: Game Initialization
        self.assertEqual(self.game.current_player, 'X', "The first player should be X")
        for row in self.game.board:
            for cell in row:
                self.assertEqual(cell, '', "The board should be empty at the start")

    def test_player_turn_alternation(self):
        # Functionality 2: Player Turn Alternation
        self.game.play_move(0, 0)  # X
        self.assertEqual(self.game.current_player, 'O', "After X plays, it should be O's turn")
        self.game.play_move(1, 1)  # O
        self.assertEqual(self.game.current_player, 'X', "After O plays, it should be X's turn")
        self.game.play_move(0, 1)  # X
        self.assertEqual(self.game.current_player, 'O', "After X plays, it should be O's turn again")

    def test_check_for_winner(self):
        # Functionality 3: Check for a Winner
        self.game.play_move(0, 0)  # X
        self.game.play_move(1, 1)  # O
        self.game.play_move(0, 1)  # X
        self.game.play_move(2, 0)  # O
        result = self.game.play_move(0, 2)  # X
        self.assertEqual(result, "X wins!", "Player X should win with a horizontal line at the top")

    def test_check_for_draw(self):
        # Functionality 4: Check for a Draw
        moves = [(0, 0), (0, 1), (1, 1), (2, 0), (1, 0), (1, 2), (2, 1), (0, 2), (2, 2)]
        players = ['X', 'O'] * 5
        for move, player in zip(moves, players):
            self.game.current_player = player
            self.game.play_move(*move)
        result = self.game.play_move(2, 2)  # Last move to fill the board
        self.assertEqual(result, "It's a draw!", "The game should end in a draw")

    def test_restart_game(self):
        # Functionality 5: Restart the Game
        self.game.play_move(0, 0)  # X
        self.game.restart()
        self.assertEqual(self.game.current_player, 'X', "The first player should be X after restart")
        for row in self.game.board:
            for cell in row:
                self.assertEqual(cell, '', "The board should be empty after restart")

    def test_timer_functionality(self):
        # Functionality 6: Timer Functionality
        self.game.start_timer()
        self.assertTrue(1.0 <= self.game.timer <= 5.0, "Timer should be between 1.0 and 5.0 seconds")

    def test_data_storage(self):
        # Functionality 7: Data Storage (not implemented in codebase)
        self.fail("Data storage functionality is not implemented in the codebase")

    def test_user_feedback_at_game_end(self):
        # Functionality 8: User Feedback at Game End (not implemented in codebase)
        self.fail("User feedback functionality is not implemented in the codebase")

    def test_invalid_move_handling(self):
        # Functionality 9: Invalid Move Handling
        self.game.play_move(0, 0)  # X
        result = self.game.play_move(0, 0)  # X tries to play again in the same cell
        self.assertEqual(result, "Move played.", "The game should prevent placing a move in an occupied cell")

if __name__ == '__main__':
    unittest.main()
