import unittest
import random
from game import Game

class Test2048Game(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()
        self.game.initialize_board()

    def test_initialize_game_board(self):
        # Functionalities 1 Test the initialization of the game board
        self.assertEqual(len(self.game.board), 4, "Board should have 4 rows")
        for row in self.game.board:
            self.assertEqual(len(row), 4, "Each row should have 4 columns")
        # Check if there are exactly two tiles with values (2 or 4)
        non_empty_tiles = sum(1 for row in self.game.board for tile in row if tile != 0)
        self.assertEqual(non_empty_tiles, 2, "There should be exactly two non-empty tiles")

    def test_move_tiles_up(self):
        # Functionalities 2 Test moving tiles up
        self.game.board = [
            [2, 2, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move("up")
        self.assertEqual(self.game.board, [
            [4, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ], "Tiles should combine correctly when moved up")

    def test_move_tiles_down(self):
        # Functionalities 3 Test moving tiles down
        self.game.board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 2, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move("down")
        self.assertEqual(self.game.board, [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [4, 0, 0, 0]
        ], "Tiles should combine correctly when moved down")

    def test_move_tiles_left(self):
        # Functionalities 4 Test moving tiles left
        self.game.board = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [2, 0, 2, 0],
            [0, 0, 0, 0]
        ]
        self.game.move("left")
        self.assertEqual(self.game.board, [
            [4, 0, 0, 0],
            [0, 0, 0, 0],
            [4, 0, 0, 0],
            [0, 0, 0, 0]
        ], "Tiles should combine correctly when moved left")

    def test_move_tiles_right(self):
        # Functionalities 5 Test moving tiles right
        self.game.board = [
            [0, 0, 2, 2],
            [0, 0, 0, 0],
            [0, 2, 0, 2],
            [0, 0, 0, 0]
        ]
        self.game.move("right")
        self.assertEqual(self.game.board, [
            [0, 0, 0, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 4],
            [0, 0, 0, 0]
        ], "Tiles should combine correctly when moved right")

    def test_generate_new_tile(self):
        # Functionalities 6 Test new tile generation after a move
        self.game.board = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move("left")
        # Check if a new tile is generated
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.game.board[i][j] == 0]
        self.assertGreater(len(empty_tiles), 0, "There should be at least one empty tile after the move")
        new_tile_found = any(self.game.board[i][j] in [2, 4] for i, j in empty_tiles)
        self.assertTrue(new_tile_found, "A new tile should be generated after the move")

    def test_check_game_over_condition(self):
        # Functionalities 7 Test game over condition
        self.game.board = [
            [2, 2, 4, 4],
            [4, 4, 2, 2],
            [2, 2, 4, 4],
            [4, 4, 2, 2]
        ]
        self.assertTrue(self.game.check_game_over(), "Game should be over when no moves are left")

    def test_save_game_state(self):
        # Functionalities 8 Test saving game state
        self.game.score = 16
        self.game.board = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.save_game_state("test_game_state.txt")
        with open("test_game_state.txt", 'r') as f:
            lines = f.readlines()
            self.assertEqual(int(lines[0].strip()), 16, "Score should be saved correctly")
            for i in range(4):
                self.assertEqual(list(map(int, lines[i + 1].strip().split(','))), self.game.board[i], "Board state should be saved correctly")

    def test_load_game_state(self):
        # Functionalities 9 Test loading game state
        self.game.save_game_state("test_game_state.txt")
        new_game = Game()
        new_game.load_game_state("test_game_state.txt")
        self.assertEqual(new_game.score, 16, "Score should be loaded correctly")
        self.assertEqual(new_game.board, self.game.board, "Board state should be loaded correctly")

if __name__ == '__main__':
    unittest.main()
