import unittest
from game import Game
from tile import Tile

class Test2048Game(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_initialize_game_board(self):
        # Functionalities 1: Initialize Game Board
        non_empty_tiles = sum(tile.value != 0 for row in self.game.board for tile in row)
        self.assertEqual(non_empty_tiles, 2, "Game should start with exactly two tiles")

    def test_move_tiles_up(self):
        # Functionalities 2: Move Tiles Up
        self.game.board = [
            [Tile(2), Tile(0), Tile(0), Tile(2)],
            [Tile(2), Tile(0), Tile(0), Tile(2)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)]
        ]
        self.game.move('up')
        self.assertEqual(self.game.board[0][0].value, 4, "Tiles should combine upwards")
        self.assertEqual(self.game.board[0][3].value, 4, "Tiles should combine upwards")

    def test_move_tiles_down(self):
        # Functionalities 3: Move Tiles Down
        self.game.board = [
            [Tile(2), Tile(0), Tile(0), Tile(2)],
            [Tile(2), Tile(0), Tile(0), Tile(2)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)]
        ]
        self.game.move('down')
        self.assertEqual(self.game.board[3][0].value, 4, "Tiles should combine downwards")
        self.assertEqual(self.game.board[3][3].value, 4, "Tiles should combine downwards")

    def test_move_tiles_left(self):
        # Functionalities 4: Move Tiles Left
        self.game.board = [
            [Tile(2), Tile(2), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)]
        ]
        self.game.move('left')
        self.assertEqual(self.game.board[0][0].value, 4, "Tiles should combine to the left")

    def test_move_tiles_right(self):
        # Functionalities 5: Move Tiles Right
        self.game.board = [
            [Tile(2), Tile(2), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)]
        ]
        self.game.move('right')
        self.assertEqual(self.game.board[0][3].value, 4, "Tiles should combine to the right")

    def test_generate_new_tile(self):
        # Functionalities 6: Generate New Tile
        self.game.board = [
            [Tile(2), Tile(2), Tile(2), Tile(2)],
            [Tile(2), Tile(2), Tile(2), Tile(2)],
            [Tile(2), Tile(2), Tile(2), Tile(2)],
            [Tile(2), Tile(2), Tile(2), Tile(0)]
        ]
        self.game.move('right')
        non_empty_tiles = sum(tile.value != 0 for row in self.game.board for tile in row)
        self.assertEqual(non_empty_tiles, 16, "A new tile should be generated after a move")

    def test_check_game_over_condition(self):
        # Functionalities 7: Check Game Over Condition
        self.game.board = [
            [Tile(2), Tile(4), Tile(2), Tile(4)],
            [Tile(4), Tile(2), Tile(4), Tile(2)],
            [Tile(2), Tile(4), Tile(2), Tile(4)],
            [Tile(4), Tile(2), Tile(4), Tile(2)]
        ]
        self.assertTrue(self.game.check_game_over(), "Game should be over when no moves are possible")

    def test_save_game_state(self):
        # Functionalities 8: Save Game State
        self.game.save_game('test_game_state.txt')
        with open('test_game_state.txt', 'r') as file:
            data = file.read().strip()
        expected_data = ','.join(str(tile.value) for row in self.game.board for tile in row) + ',' + str(self.game.score)
        self.assertEqual(data, expected_data, "Game state should be saved correctly")

    def test_load_game_state(self):
        # Functionalities 9: Load Game State
        self.game.save_game('test_game_state.txt')
        self.game.board = [[Tile(0)] * 4 for _ in range(4)]  # Reset board
        self.game.load_game('test_game_state.txt')
        loaded_data = ','.join(str(tile.value) for row in self.game.board for tile in row) + ',' + str(self.game.score)
        with open('test_game_state.txt', 'r') as file:
            expected_data = file.read().strip()
        self.assertEqual(loaded_data, expected_data, "Game state should be loaded correctly")

if __name__ == '__main__':
    unittest.main()
