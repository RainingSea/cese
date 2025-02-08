import unittest
from game import Game, Block

class TestBlockConnectGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_select_and_connect_blocks(self):
        # Functionalities 1: Select and Connect Blocks of the Same Color
        initial_score = self.game.score
        self.game.select_block(0, 0)  # Select a red block
        self.assertEqual(self.game.score, initial_score + 3, "Score should increase by 3 after clearing red blocks")
        for row in self.game.grid:
            for block in row:
                self.assertNotEqual(block.color, "red", "Red blocks should be cleared from the grid")

    def test_display_game_grid(self):
        # Functionalities 2: Display the Game Grid
        # Since this is a visual test, we will check if the grid is initialized correctly
        expected_colors = [["red", "green", "blue"],
                           ["green", "blue", "red"],
                           ["blue", "red", "green"]]
        actual_colors = [[block.color for block in row] for row in self.game.grid]
        self.assertEqual(actual_colors, expected_colors, "Initial grid colors should match expected colors")

    def test_score_calculation_after_block_clearing(self):
        # Functionalities 3: Score Calculation After Block Clearing
        initial_score = self.game.score
        self.game.select_block(0, 0)  # Select a red block
        self.assertEqual(self.game.score, initial_score + 3, "Score should increase by 3 after clearing red blocks")

    def test_blocks_fall_to_occupy_spaces(self):
        # Functionalities 4: Blocks Fall to Occupy Spaces
        # This functionality is not implemented in the codebase
        self.fail("Block falling logic is not implemented in the codebase")

    def test_undo_last_move(self):
        # Functionalities 5: Undo Last Move
        self.game.select_block(0, 0)  # Select a red block
        score_after_selection = self.game.score
        self.game.undo()
        self.assertEqual(self.game.score, score_after_selection - 3, "Score should decrease by 3 after undo")
        self.assertEqual(self.game.grid[0][0].color, "red", "Red block should be restored after undo")

    def test_save_game_state(self):
        # Functionalities 6: Save Game State to a Local File
        try:
            self.game.save_state()
            with open('game_state.txt', 'r') as f:
                state = f.read()
            self.assertIn('"score": 0', state, "Game state should be saved with initial score")
        except Exception as e:
            self.fail(f"Saving game state raised an exception: {e}")

    def test_load_game_state(self):
        # Functionalities 7: Load Game State from a Local File
        self.game.select_block(0, 0)  # Change the game state
        self.game.load_state()  # Load the initial state
        self.assertEqual(self.game.score, 0, "Score should be reset to 0 after loading initial state")
        expected_colors = [["red", "green", "blue"],
                           ["green", "blue", "red"],
                           ["blue", "red", "green"]]
        actual_colors = [[block.color for block in row] for row in self.game.grid]
        self.assertEqual(actual_colors, expected_colors, "Grid colors should match initial state after loading")

if __name__ == '__main__':
    unittest.main()
