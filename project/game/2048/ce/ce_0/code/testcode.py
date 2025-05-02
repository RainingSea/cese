import unittest
from game import Game

class Test2048Game(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()
        self.game.start_game()

    def test_initialize_game_board(self):
        # Functionalities 1: Check if the game board is initialized correctly
        self.assertEqual(len(self.game.board.tiles), 4, "Board should have 4 rows")
        self.assertEqual(len(self.game.board.tiles[0]), 4, "Board should have 4 columns")
        empty_count = sum(tile == 0 for row in self.game.board.tiles for tile in row)
        self.assertEqual(empty_count, 14, "There should be 14 empty tiles after initialization")
        self.assertEqual(sum(tile for row in self.game.board.tiles for tile in row), 4, "Sum of tiles should be 4 (two '2' tiles)")

    def test_move_tiles_up(self):
        # Functionalities 2: Test moving tiles up
        self.game.board.tiles = [
            [2, 2, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move('up')
        expected_tiles = [
            [4, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game.board.tiles, expected_tiles, "Tiles should merge correctly when moved up")

    def test_move_tiles_down(self):
        # Functionalities 3: Test moving tiles down
        self.game.board.tiles = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 2, 0, 0],
            [2, 0, 0, 0]
        ]
        self.game.move('down')
        expected_tiles = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [4, 0, 0, 0]
        ]
        self.assertEqual(self.game.board.tiles, expected_tiles, "Tiles should merge correctly when moved down")

    def test_move_tiles_left(self):
        # Functionalities 4: Test moving tiles left
        self.game.board.tiles = [
            [2, 2, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move('left')
        expected_tiles = [
            [4, 0, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game.board.tiles, expected_tiles, "Tiles should merge correctly when moved left")

    def test_move_tiles_right(self):
        # Functionalities 5: Test moving tiles right
        self.game.board.tiles = [
            [0, 0, 2, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move('right')
        expected_tiles = [
            [0, 0, 0, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game.board.tiles, expected_tiles, "Tiles should merge correctly when moved right")

    def test_generate_new_tile(self):
        # Functionalities 6: Check if a new tile is generated after a move
        self.game.board.tiles = [
            [2, 2, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move('left')
        new_tile_count = sum(tile in (2, 4) for row in self.game.board.tiles for tile in row)
        self.assertGreater(new_tile_count, 0, "A new tile should be generated after a valid move")

    def test_check_game_over_condition(self):
        # Functionalities 7: Check game over condition
        self.game.board.tiles = [
            [2, 2, 4, 4],
            [4, 4, 2, 2],
            [2, 2, 4, 4],
            [4, 4, 2, 2]
        ]
        self.assertTrue(self.game.check_game_over(), "Game should be over when no moves are left")

    def test_save_game_state(self):
        # Functionalities 8: Test saving game state
        self.game.board.tiles = [
            [2, 2, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.save_game()
        with open('game_state.txt', 'r') as file:
            lines = file.readlines()
            self.assertEqual(lines[0].strip(), "2,2,0,0", "First row should match saved state")
            self.assertEqual(lines[1].strip(), "2,0,0,0", "Second row should match saved state")

    def test_load_game_state(self):
        # Functionalities 9: Test loading game state
        self.game.board.tiles = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.load_game()
        self.assertEqual(self.game.board.tiles[0], [2, 2, 0, 0], "First row should match loaded state")
        self.assertEqual(self.game.board.tiles[1], [2, 0, 0, 0], "Second row should match loaded state")

if __name__ == '__main__':
    unittest.main()
