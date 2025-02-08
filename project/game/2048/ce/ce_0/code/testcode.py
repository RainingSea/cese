import unittest
from game import Game, Tile

class Test2048Game(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_initialize_game_board(self):
        # Functionalities 1: Initialize Game Board
        self.game.start_game()
        non_empty_tiles = sum(tile.value != 0 for row in self.game.board for tile in row)
        self.assertEqual(non_empty_tiles, 2, "Game board should start with two non-empty tiles")

    def test_move_tiles_up(self):
        # Functionalities 2: Move Tiles Up
        self.game.board = [
            [Tile(2), Tile(0), Tile(0), Tile(2)],
            [Tile(2), Tile(0), Tile(0), Tile(2)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)]
        ]
        self.game.move('up')
        expected_board = [
            [Tile(4), Tile(0), Tile(0), Tile(4)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)]
        ]
        self.assertEqual(self.game.board, expected_board, "Tiles should combine and move up correctly")

    def test_move_tiles_down(self):
        # Functionalities 3: Move Tiles Down
        self.game.board = [
            [Tile(2), Tile(0), Tile(0), Tile(2)],
            [Tile(2), Tile(0), Tile(0), Tile(2)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)]
        ]
        self.game.move('down')
        expected_board = [
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(4), Tile(0), Tile(0), Tile(4)],
            [Tile(0), Tile(0), Tile(0), Tile(0)]
        ]
        self.assertEqual(self.game.board, expected_board, "Tiles should combine and move down correctly")

    def test_move_tiles_left(self):
        # Functionalities 4: Move Tiles Left
        self.game.board = [
            [Tile(2), Tile(2), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)]
        ]
        self.game.move('left')
        expected_board = [
            [Tile(4), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)]
        ]
        self.assertEqual(self.game.board, expected_board, "Tiles should combine and move left correctly")

    def test_move_tiles_right(self):
        # Functionalities 5: Move Tiles Right
        self.game.board = [
            [Tile(0), Tile(0), Tile(2), Tile(2)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)]
        ]
        self.game.move('right')
        expected_board = [
            [Tile(0), Tile(0), Tile(0), Tile(4)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)],
            [Tile(0), Tile(0), Tile(0), Tile(0)]
        ]
        self.assertEqual(self.game.board, expected_board, "Tiles should combine and move right correctly")

    def test_generate_new_tile(self):
        # Functionalities 6: Generate New Tile
        self.game.board = [
            [Tile(2), Tile(2), Tile(2), Tile(2)],
            [Tile(2), Tile(2), Tile(2), Tile(2)],
            [Tile(2), Tile(2), Tile(2), Tile(2)],
            [Tile(0), Tile(0), Tile(0), Tile(0)]
        ]
        self.game.spawn_tile()
        non_empty_tiles = sum(tile.value != 0 for row in self.game.board for tile in row)
        self.assertEqual(non_empty_tiles, 13, "A new tile should be generated on the board")

    def test_check_game_over_condition(self):
        # Functionalities 7: Check Game Over Condition
        self.game.board = [
            [Tile(2), Tile(4), Tile(2), Tile(4)],
            [Tile(4), Tile(2), Tile(4), Tile(2)],
            [Tile(2), Tile(4), Tile(2), Tile(4)],
            [Tile(4), Tile(2), Tile(4), Tile(2)]
        ]
        game_over = self.game.check_game_over()
        self.assertTrue(game_over, "Game should be over when no moves are possible")

    def test_save_game_state(self):
        # Functionalities 8: Save Game State
        self.game.board = [
            [Tile(2), Tile(4), Tile(2), Tile(4)],
            [Tile(4), Tile(2), Tile(4), Tile(2)],
            [Tile(2), Tile(4), Tile(2), Tile(4)],
            [Tile(4), Tile(2), Tile(4), Tile(2)]
        ]
        self.game.save_game_state()
        with open('game_state.txt', 'r') as f:
            lines = f.readlines()
        self.assertEqual(lines[0].strip(), '0', "Score should be saved correctly")
        self.assertEqual(lines[1].strip(), '2|4|2|4', "Game state should be saved correctly")

    def test_load_game_state(self):
        # Functionalities 9: Load Game State
        with open('game_state.txt', 'w') as f:
            f.write("0\n2|4|2|4\n4|2|4|2\n2|4|2|4\n4|2|4|2\n")
        self.game.load_game_state()
        expected_board = [
            [Tile(2), Tile(4), Tile(2), Tile(4)],
            [Tile(4), Tile(2), Tile(4), Tile(2)],
            [Tile(2), Tile(4), Tile(2), Tile(4)],
            [Tile(4), Tile(2), Tile(4), Tile(2)]
        ]
        self.assertEqual(self.game.board, expected_board, "Game state should be loaded correctly")

if __name__ == '__main__':
    unittest.main()
