import unittest
from game import Game

class Test2048Game(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_initialize_game_board(self):
        # Functionalities 1: Initialize Game Board
        non_zero_tiles = sum(tile != 0 for row in self.game.board for tile in row)
        self.assertEqual(non_zero_tiles, 2, "The game should start with exactly two tiles on the board.")

    def test_move_tiles_up(self):
        # Functionalities 2: Move Tiles Up
        self.game.board = [
            [2, 0, 0, 2],
            [2, 0, 0, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move('up')
        expected_board = [
            [4, 0, 0, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game.board, expected_board, "Tiles should combine and move up correctly.")

    def test_move_tiles_down(self):
        # Functionalities 3: Move Tiles Down
        self.game.board = [
            [2, 0, 0, 2],
            [2, 0, 0, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move('down')
        expected_board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [4, 0, 0, 4]
        ]
        self.assertEqual(self.game.board, expected_board, "Tiles should combine and move down correctly.")

    def test_move_tiles_left(self):
        # Functionalities 4: Move Tiles Left
        self.game.board = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 2, 0, 0]
        ]
        self.game.move('left')
        expected_board = [
            [4, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [4, 0, 0, 0]
        ]
        self.assertEqual(self.game.board, expected_board, "Tiles should combine and move left correctly.")

    def test_move_tiles_right(self):
        # Functionalities 5: Move Tiles Right
        self.game.board = [
            [0, 0, 2, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 2, 2]
        ]
        self.game.move('right')
        expected_board = [
            [0, 0, 0, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 4]
        ]
        self.assertEqual(self.game.board, expected_board, "Tiles should combine and move right correctly.")

    def test_generate_new_tile(self):
        # Functionalities 6: Generate New Tile
        self.game.board = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [0, 0, 0, 0]
        ]
        self.game.generate_tile()
        non_zero_tiles = sum(tile != 0 for row in self.game.board for tile in row)
        self.assertEqual(non_zero_tiles, 13, "A new tile should be generated after a move.")

    def test_check_game_over_condition(self):
        # Functionalities 7: Check Game Over Condition
        self.game.board = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [2, 4, 8, 16]
        ]
        self.assertTrue(self.game.check_game_over(), "Game should be over when no moves are possible.")

    def test_save_game_state(self):
        # Functionalities 8: Save Game State
        self.game.board = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [2, 4, 8, 16]
        ]
        self.game.save_game('test_game_state.txt')
        with open('test_game_state.txt', 'r') as f:
            lines = f.readlines()
        expected_lines = [
            'score: 0\n',
            '2,4,8,16\n',
            '32,64,128,256\n',
            '512,1024,2048,4096\n',
            '2,4,8,16\n'
        ]
        self.assertEqual(lines, expected_lines, "Game state should be saved correctly to the file.")

    def test_load_game_state(self):
        # Functionalities 9: Load Game State
        with open('test_game_state.txt', 'w') as f:
            f.writelines([
                'score: 0\n',
                '2,4,8,16\n',
                '32,64,128,256\n',
                '512,1024,2048,4096\n',
                '2,4,8,16\n'
            ])
        self.game.load_game('test_game_state.txt')
        expected_board = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [2, 4, 8, 16]
        ]
        self.assertEqual(self.game.board, expected_board, "Game state should be loaded correctly from the file.")

if __name__ == '__main__':
    unittest.main()
