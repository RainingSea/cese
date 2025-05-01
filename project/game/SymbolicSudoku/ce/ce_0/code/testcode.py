import unittest
from game import Game

class TestSymbolicSudokuGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_fill_grid_with_symbols(self):
        # Test filling an empty cell with a symbol
        self.game.grid.input_symbol('A', 0, 0)
        self.assertEqual(self.game.grid.cells[0][0], 'A', "Symbol 'A' should be in cell (0, 0)")

        # Test attempting to fill a cell that is already filled
        self.game.grid.input_symbol('B', 0, 0)
        self.assertEqual(self.game.grid.cells[0][0], 'A', "Cell (0, 0) should still contain 'A'")

    def test_unique_symbols_in_rows_columns_subgrids(self):
        # Fill a row with unique symbols
        for i in range(9):
            self.game.grid.input_symbol(chr(65 + i), 0, i)  # Fill row 0 with 'A' to 'I'

        # Attempt to input a duplicate symbol in the same row
        self.game.grid.input_symbol('A', 0, 1)
        self.assertEqual(self.game.grid.cells[0][1], 'B', "Cell (0, 1) should still contain 'B'")

        # Fill a column with unique symbols
        for i in range(9):
            self.game.grid.input_symbol(chr(65 + i), i, 0)  # Fill column 0 with 'A' to 'I'

        # Attempt to input a duplicate symbol in the same column
        self.game.grid.input_symbol('A', 1, 0)
        self.assertEqual(self.game.grid.cells[1][0], 'B', "Cell (1, 0) should still contain 'B'")

    def test_multiple_difficulty_levels(self):
        # Test loading an easy puzzle
        self.game.difficulty.set_difficulty('Easy')
        self.game.load_puzzle()
        self.assertNotEqual(self.game.grid.cells, [[0]*9]*9, "Easy puzzle should load with some filled cells")

        # Test loading a hard puzzle
        self.game.difficulty.set_difficulty('Hard')
        self.game.load_puzzle()
        self.assertNotEqual(self.game.grid.cells, [[0]*9]*9, "Hard puzzle should load with some filled cells")

    def test_input_symbols_using_mouse_or_keyboard(self):
        # Simulate inputting a symbol using the keyboard
        self.game.grid.input_symbol('C', 1, 1)
        self.assertEqual(self.game.grid.cells[1][1], 'C', "Symbol 'C' should be in cell (1, 1)")

        # Simulate inputting a symbol using mouse click (not implemented)
        self.fail("Mouse input functionality is not implemented in the codebase")

    def test_track_time_taken_to_solve_puzzle(self):
        # Start a game and simulate solving the puzzle
        self.game.start_game()
        self.game.timer.stop()  # Simulate completing the puzzle
        time_taken = self.game.timer.get_time()
        self.assertIsNotNone(time_taken, "Time taken should be recorded")

    def test_reset_puzzle(self):
        # Fill some cells
        self.game.grid.input_symbol('D', 2, 2)
        self.assertEqual(self.game.grid.cells[2][2], 'D', "Cell (2, 2) should contain 'D'")

        # Reset the game
        self.game.reset_game()
        self.assertEqual(self.game.grid.cells[2][2], 0, "Cell (2, 2) should be reset to 0")

if __name__ == '__main__':
    unittest.main()
