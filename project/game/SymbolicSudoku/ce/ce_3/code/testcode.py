import unittest
from game import Game, Difficulty

class TestSymbolicSudokuGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()
        self.game.start_game(Difficulty.EASY)

    def test_fill_grid_with_symbols(self):
        # Functionalities 1: Fill a 9x9 Grid with Symbols
        # Test inputting a symbol in an empty cell
        self.assertTrue(self.game.input_symbol(0, 0, 'A'), "Should be able to input 'A' in an empty cell")
        self.assertEqual(self.game.grid.cells[0][0], 'A', "Cell should contain 'A' after input")

        # Test inputting a symbol in a filled cell
        self.assertFalse(self.game.input_symbol(0, 0, 'B'), "Should not be able to input 'B' in a filled cell")
        self.assertEqual(self.game.grid.cells[0][0], 'A', "Cell should still contain 'A'")

    def test_unique_symbols_in_rows_columns_subgrids(self):
        # Functionalities 2: Ensure Unique Symbols in Rows, Columns, and Subgrids
        # Fill a row with unique symbols
        symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        for col, symbol in enumerate(symbols):
            self.assertTrue(self.game.input_symbol(0, col, symbol), f"Should be able to input '{symbol}' in row 0")

        # Attempt to input a duplicate symbol in the same row
        self.assertFalse(self.game.input_symbol(0, 1, 'A'), "Should not be able to input duplicate 'A' in the same row")

        # Fill a column with unique symbols
        for row, symbol in enumerate(symbols):
            self.assertTrue(self.game.input_symbol(row, 0, symbol), f"Should be able to input '{symbol}' in column 0")

        # Attempt to input a duplicate symbol in the same column
        self.assertFalse(self.game.input_symbol(1, 0, 'A'), "Should not be able to input duplicate 'A' in the same column")

    def test_multiple_difficulty_levels(self):
        # Functionalities 3: Multiple Difficulty Levels
        # Start a new game with 'Easy' difficulty
        self.game.start_game(Difficulty.EASY)
        self.assertEqual(self.game.difficulty, Difficulty.EASY, "Game should start with 'Easy' difficulty")

        # Start a new game with 'Hard' difficulty
        self.game.start_game(Difficulty.HARD)
        self.assertEqual(self.game.difficulty, Difficulty.HARD, "Game should start with 'Hard' difficulty")

    def test_input_symbols_using_mouse_or_keyboard(self):
        # Functionalities 4: Input Symbols Using Mouse Click or Keyboard
        # This functionality is not implemented in the codebase
        self.fail("Input symbols using mouse click or keyboard functionality is not implemented in the codebase")

    def test_track_time_taken_to_solve_puzzle(self):
        # Functionalities 5: Track Time Taken to Solve Each Puzzle
        self.game.timer.start()
        time.sleep(1)  # Simulate time passing
        elapsed_time = self.game.timer.stop()
        self.assertGreater(elapsed_time, 0, "Elapsed time should be greater than 0")

    def test_reset_puzzle(self):
        # Functionalities 6: Reset the Puzzle
        self.game.input_symbol(0, 0, 'A')
        self.game.reset_game()
        self.assertEqual(self.game.grid.cells[0][0], '', "Grid should be reset to initial state")

if __name__ == '__main__':
    unittest.main()
