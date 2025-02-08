import unittest
from game import Game

class Test2048Game(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_initialize_game_board(self):
        # Functionalities 1: Initialize Game Board
        non_empty_tiles = sum(tile != 0 for row in self.game.board for tile in row)
        self.assertEqual(non_empty_tiles, 2, "Game should start with exactly two tiles on the board")

    def test_move_tiles_up(self):
        # Functionalities 2: Move Tiles Up
        self.game.board = [
            [2, 0, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move('w')
        self.assertEqual(self.game.board[0][0], 4, "Tiles should merge upwards")
        self.assertEqual(self.game.board[1][0], 0, "Second row should be empty after merge")

    def test_move_tiles_down(self):
        # Functionalities 3: Move Tiles Down
        self.game.board = [
            [2, 0, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move('s')
        self.assertEqual(self.game.board[3][0], 4, "Tiles should merge downwards")
        self.assertEqual(self.game.board[2][0], 0, "Third row should be empty after merge")

    def test_move_tiles_left(self):
        # Functionalities 4: Move Tiles Left
        self.game.board = [
            [0, 0, 2, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move('a')
        self.assertEqual(self.game.board[0][0], 4, "Tiles should merge to the left")
        self.assertEqual(self.game.board[0][1], 0, "Second column should be empty after merge")

    def test_move_tiles_right(self):
        # Functionalities 5: Move Tiles Right
        self.game.board = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move('d')
        self.assertEqual(self.game.board[0][3], 4, "Tiles should merge to the right")
        self.assertEqual(self.game.board[0][2], 0, "Third column should be empty after merge")

    def test_generate_new_tile(self):
        # Functionalities 6: Generate New Tile
        initial_empty_tiles = sum(tile == 0 for row in self.game.board for tile in row)
        self.game.move('w')  # Make a move to trigger tile generation
        new_empty_tiles = sum(tile == 0 for row in self.game.board for tile in row)
        self.assertEqual(initial_empty_tiles - 1, new_empty_tiles, "A new tile should be generated after a move")

    def test_check_game_over_condition(self):
        # Functionalities 7: Check Game Over Condition
        self.game.board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]
        self.game.check_game_over()
        self.assertTrue(self.game.game_over, "Game should be over when no moves are possible")

    def test_save_game_state(self):
        # Functionalities 8: Save Game State
        self.game.save_game('test_save.json')
        with open('test_save.json', 'r') as f:
            data = f.read()
        self.assertIn('"board":', data, "Game state should be saved to file")
        self.assertIn('"score":', data, "Score should be saved to file")

    def test_load_game_state(self):
        # Functionalities 9: Load Game State
        self.game.save_game('test_save.json')
        self.game.board = [[0] * 4 for _ in range(4)]  # Clear the board
        self.game.load_game('test_save.json')
        non_empty_tiles = sum(tile != 0 for row in self.game.board for tile in row)
        self.assertEqual(non_empty_tiles, 2, "Game state should be loaded from file")

if __name__ == '__main__':
    unittest.main()
