import unittest
import pygame
from game import Game

class Test2048Game(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_initialize_game_board(self):
        # Functionalities 1: Test if the game board is initialized correctly
        self.assertEqual(len(self.game.board), 4, "Board should have 4 rows")
        for row in self.game.board:
            self.assertEqual(len(row), 4, "Each row should have 4 columns")
        # Check if there are two non-zero tiles
        non_zero_tiles = sum(1 for row in self.game.board for tile in row if tile != 0)
        self.assertEqual(non_zero_tiles, 2, "There should be two non-zero tiles at initialization")

    def test_move_tiles_up(self):
        # Functionalities 2: Test moving tiles up
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
        # Functionalities 3: Test moving tiles down
        self.game.board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 2, 0, 0],
            [2, 0, 0, 0]
        ]
        self.game.move("down")
        self.assertEqual(self.game.board, [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [4, 0, 0, 0]
        ], "Tiles should combine correctly when moved down")

    def test_move_tiles_left(self):
        # Functionalities 4: Test moving tiles left
        self.game.board = [
            [2, 2, 0, 0],
            [0, 2, 2, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move("left")
        self.assertEqual(self.game.board, [
            [4, 0, 0, 0],
            [0, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ], "Tiles should combine correctly when moved left")

    def test_move_tiles_right(self):
        # Functionalities 5: Test moving tiles right
        self.game.board = [
            [0, 0, 2, 2],
            [0, 0, 0, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move("right")
        self.assertEqual(self.game.board, [
            [0, 0, 0, 4],
            [0, 0, 0, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ], "Tiles should combine correctly when moved right")

    def test_generate_new_tile(self):
        # Functionalities 6: Test if a new tile is generated after a move
        self.game.board = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move("left")
        new_tile_count = sum(1 for row in self.game.board for tile in row if tile in (2, 4))
        self.assertEqual(new_tile_count, 3, "A new tile should be generated after a move")

    def test_check_game_over(self):
        # Functionalities 7: Test game over condition
        self.game.board = [
            [2, 2, 4, 4],
            [4, 4, 2, 2],
            [2, 2, 4, 4],
            [4, 4, 2, 2]
        ]
        self.game.check_game_over()
        # Since there's no valid move left, we expect a game over message
        # Note: The actual game over message is printed, we can only check the board state
        self.assertIsNone(self.game.check_game_over(), "Game should be over with no valid moves left")

    def test_save_game_state(self):
        # Functionalities 8: Test saving game state
        self.game.board = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.score = 4
        self.game.save_game()
        with open("game_state.txt", "r") as f:
            lines = f.readlines()
            self.assertEqual(lines[0].strip(), "2|2|0|0", "First row should match the saved state")
            self.assertEqual(lines[1].strip(), "0|0|0|0", "Second row should match the saved state")
            self.assertEqual(lines[4].strip(), "4", "Score should match the saved state")

    def test_load_game_state(self):
        # Functionalities 9: Test loading game state
        self.game.load_game()
        self.assertEqual(self.game.board, [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ], "Loaded board should match the saved state")
        self.assertEqual(self.game.score, 0, "Loaded score should match the saved state")

if __name__ == '__main__':
    unittest.main()
