import unittest
import os
from main import Game

class Test2048Game(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_initialize_game_board(self):
        # Functionalities 1: Check if the game board is initialized correctly
        self.assertEqual(len(self.game.board), 4, "Board should have 4 rows")
        for row in self.game.board:
            self.assertEqual(len(row), 4, "Each row should have 4 columns")
        self.assertEqual(sum(sum(row) for row in self.game.board), 4, "Initial score should be 4 (two '2' tiles)")

    def test_move_tiles_up(self):
        # Functionalities 2: Test moving tiles up
        self.game.board = [
            [2, 2, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move('up')
        expected_board = [
            [4, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game.board, expected_board, "Tiles should combine correctly when moved up")

    def test_move_tiles_down(self):
        # Functionalities 3: Test moving tiles down
        self.game.board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 2, 0, 0],
            [2, 0, 0, 0]
        ]
        self.game.move('down')
        expected_board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [4, 0, 0, 0]
        ]
        self.assertEqual(self.game.board, expected_board, "Tiles should combine correctly when moved down")

    def test_move_tiles_left(self):
        # Functionalities 4: Test moving tiles left
        self.game.board = [
            [2, 2, 0, 0],
            [0, 2, 2, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move('left')
        expected_board = [
            [4, 0, 0, 0],
            [0, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game.board, expected_board, "Tiles should combine correctly when moved left")

    def test_move_tiles_right(self):
        # Functionalities 5: Test moving tiles right
        self.game.board = [
            [0, 0, 2, 2],
            [0, 0, 0, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.move('right')
        expected_board = [
            [0, 0, 0, 4],
            [0, 0, 0, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game.board, expected_board, "Tiles should combine correctly when moved right")

    def test_generate_new_tile(self):
        # Functionalities 6: Test new tile generation
        self.game.board = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.generate_tile()
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.game.board[i][j] == 0]
        self.assertTrue(len(empty_cells) < 16, "A new tile should be generated in an empty cell")

    def test_check_game_over(self):
        # Functionalities 7: Test game over condition
        self.game.board = [
            [2, 2, 4, 4],
            [2, 2, 4, 4],
            [4, 4, 2, 2],
            [4, 4, 2, 2]
        ]
        self.assertTrue(self.game.check_game_over(), "Game should be over when no moves are left")

    def test_save_game_state(self):
        # Functionalities 8: Test saving game state
        self.game.board = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.score = 4
        self.game.save_game_state('test_game_state.txt')
        self.assertTrue(os.path.exists('test_game_state.txt'), "Game state file should be created")

        with open('test_game_state.txt', 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 5, "Game state file should contain 5 lines")
            self.assertEqual(lines[-1].strip(), '4', "Last line should contain the score")

        os.remove('test_game_state.txt')  # Clean up

    def test_load_game_state(self):
        # Functionalities 9: Test loading game state
        with open('test_load_game_state.txt', 'w') as f:
            f.write("2,2,0,0\n")
            f.write("0,0,0,0\n")
            f.write("0,0,0,0\n")
            f.write("0,0,0,0\n")
            f.write("4\n")

        self.game.load_game_state('test_load_game_state.txt')
        expected_board = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(self.game.board, expected_board, "Loaded board should match saved board")
        self.assertEqual(self.game.score, 4, "Loaded score should match saved score")

        os.remove('test_load_game_state.txt')  # Clean up

if __name__ == '__main__':
    unittest.main()
