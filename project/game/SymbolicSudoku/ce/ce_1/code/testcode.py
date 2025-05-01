import unittest
from game import Game, Grid, Difficulty

class TestSymbolicSudokuGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.grid = self.game.grid
        self.difficulty = Difficulty('easy')

    def test_fill_grid_with_symbols(self):
        # Functionalities 1: Fill a 9x9 Grid with Symbols
        self.grid.fill_cell(0, 0, 'A')
        self.assertEqual(self.grid.cells[0][0], 'A', "Cell (0,0) should contain 'A'")

        # Attempt to fill an already filled cell
        self.grid.fill_cell(0, 0, 'B')
        self.assertEqual(self.grid.cells[0][0], 'A', "Cell (0,0) should still contain 'A'")

    def test_unique_symbols_in_rows_columns_subgrids(self):
        # Functionalities 2: Ensure Unique Symbols in Rows, Columns, and Subgrids
        for i in range(9):
            self.grid.fill_cell(0, i, chr(65 + i))  # Fill row 0 with 'A' to 'I'
        self.assertNotEqual(self.grid.cells[0][0], self.grid.cells[0][1], "Row should not contain duplicates")

        # Attempt to input a duplicate symbol in the same row
        self.grid.fill_cell(0, 0, 'A')
        self.assertEqual(self.grid.cells[0][0], 'A', "Cell (0,0) should still contain 'A'")

        # Fill a column with symbols
        for i in range(9):
            self.grid.fill_cell(i, 0, chr(65 + i))  # Fill column 0 with 'A' to 'I'
        self.assertNotEqual(self.grid.cells[0][0], self.grid.cells[1][0], "Column should not contain duplicates")

    def test_multiple_difficulty_levels(self):
        # Functionalities 3: Multiple Difficulty Levels
        self.game.start_game()
        self.game.load_puzzle('easy')
        self.assertEqual(self.grid.cells[0][0], 5, "Easy puzzle should load with initial symbols")

        self.game.reset_game()
        self.game.load_puzzle('hard')
        self.assertEqual(self.grid.cells[0][0], 0, "Hard puzzle should load with no initial symbols")

    def test_input_symbols_with_mouse_keyboard(self):
        # Functionalities 4: Input Symbols Using Mouse Click or Keyboard
        self.grid.fill_cell(1, 1, 'B')
        self.assertEqual(self.grid.cells[1][1], 'B', "Cell (1,1) should contain 'B' after input")

    def test_track_time_taken(self):
        # Functionalities 5: Track Time Taken to Solve Each Puzzle
        self.game.timer.start()
        self.game.timer.stop()
        elapsed_time = self.game.track_time()
        self.assertIn("seconds", elapsed_time, "Elapsed time should be displayed in seconds")

    def test_reset_puzzle(self):
        # Functionalities 6: Reset the Puzzle
        self.grid.fill_cell(0, 0, 'A')
        self.game.reset_game()
        self.assertEqual(self.grid.cells[0][0], 0, "Cell (0,0) should be cleared after reset")

if __name__ == '__main__':
    unittest.main()
