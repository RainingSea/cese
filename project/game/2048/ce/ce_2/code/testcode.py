import unittest
from game import Game
from game_board import GameBoard
from score import Score
from ui import UI

class Test2048Game(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.board = self.game.board
        self.score = self.game.score

    def test_initialize_game_board(self):
        # Functionalities 1: Initialize Game Board
        self.game.start_game()
        self.assertEqual(len(self.board.tiles), 4, "Game board should have 4 rows")
        self.assertEqual(len(self.board.tiles[0]), 4, "Game board should have 4 columns")
        self.assertEqual(sum(sum(row) for row in self.board.tiles), 2, "Initial score should be 2 (two '2' tiles)")

    def test_move_tiles_up(self):
        # Functionalities 2: Move Tiles Up
        self.board.tiles = [[2, 2, 0, 0],
                            [2, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]]
        self.game.move('up')
        self.assertEqual(self.board.tiles, [[4, 0, 0, 0],
                                             [0, 0, 0, 0],
                                             [0, 0, 0, 0],
                                             [0, 0, 0, 0]], "Tiles should combine and move up correctly")

    def test_move_tiles_down(self):
        # Functionalities 3: Move Tiles Down
        self.board.tiles = [[0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [2, 2, 0, 0],
                            [2, 0, 0, 0]]
        self.game.move('down')
        self.assertEqual(self.board.tiles, [[0, 0, 0, 0],
                                             [0, 0, 0, 0],
                                             [0, 0, 0, 0],
                                             [4, 0, 0, 0]], "Tiles should combine and move down correctly")

    def test_move_tiles_left(self):
        # Functionalities 4: Move Tiles Left
        self.board.tiles = [[2, 2, 0, 0],
                            [0, 2, 2, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]]
        self.game.move('left')
        self.assertEqual(self.board.tiles, [[4, 0, 0, 0],
                                             [0, 4, 0, 0],
                                             [0, 0, 0, 0],
                                             [0, 0, 0, 0]], "Tiles should combine and move left correctly")

    def test_move_tiles_right(self):
        # Functionalities 5: Move Tiles Right
        self.board.tiles = [[0, 0, 2, 2],
                            [0, 0, 0, 2],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]]
        self.game.move('right')
        self.assertEqual(self.board.tiles, [[0, 0, 0, 4],
                                             [0, 0, 0, 2],
                                             [0, 0, 0, 0],
                                             [0, 0, 0, 0]], "Tiles should combine and move right correctly")

    def test_generate_new_tile(self):
        # Functionalities 6: Generate New Tile
        self.board.tiles = [[2, 2, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]]
        self.game.move('left')
        new_tile_count = sum(tile != 0 for row in self.board.tiles for tile in row)
        self.assertGreater(new_tile_count, 0, "A new tile should be generated after a valid move")

    def test_check_game_over_condition(self):
        # Functionalities 7: Check Game Over Condition
        self.board.tiles = [[2, 2, 4, 4],
                            [4, 4, 2, 2],
                            [2, 2, 4, 4],
                            [4, 4, 2, 2]]
        self.assertTrue(self.game.game_over(), "Game should be over when no moves are left")

    def test_save_game_state(self):
        # Functionalities 8: Save Game State
        self.game.board.tiles = [[2, 2, 0, 0],
                                 [0, 0, 0, 0],
                                 [0, 0, 0, 0],
                                 [0, 0, 0, 0]]
        self.game.score.update_score(4)
        self.game.save_game()
        with open('game_state.txt', 'r') as file:
            lines = file.readlines()
            self.assertEqual(lines[0].strip(), '2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0', "Game state should be saved correctly")
            self.assertEqual(lines[1].strip(), 'Score: 4', "Score should be saved correctly")

    def test_load_game_state(self):
        # Functionalities 9: Load Game State
        self.game.load_game()
        self.assertEqual(self.board.tiles, [[0, 0, 2, 0],
                                             [4, 0, 0, 0],
                                             [0, 2, 0, 0],
                                             [0, 0, 0, 0]], "Game state should be loaded correctly")
        self.assertEqual(self.score.get_score(), 2048, "Score should be loaded correctly")

if __name__ == '__main__':
    unittest.main()
