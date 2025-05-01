import unittest
from game import Game
from score import Score
from grid import Grid
from block import Block

class TestBlockConnectGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.score = Score()
        self.grid = Grid()

    def test_select_and_connect_blocks(self):
        # Functionalities 1: Select and connect blocks of the same color
        # Assuming we have a way to set block colors for testing
        self.grid.blocks[0][0] = Block(color="blue")
        self.grid.blocks[0][1] = Block(color="blue")
        self.grid.blocks[0][2] = Block(color="red")  # Different color
        self.game.select_block(0, 0)  # Select first blue block
        self.game.select_block(0, 1)  # Select second blue block
        # Check if the blocks are cleared (assuming get_connected_blocks returns them)
        self.assertEqual(self.grid.get_connected_blocks(), [], "Blocks should be cleared after connection")

    def test_display_game_grid(self):
        # Functionalities 2: Display the game grid
        # This is a placeholder test since display logic is not implemented
        self.assertIsNotNone(self.grid, "Game grid should be initialized")

    def test_score_calculation_after_block_clearing(self):
        # Functionalities 3: Score calculation after block clearing
        self.grid.blocks[0][0] = Block(color="green")
        self.grid.blocks[0][1] = Block(color="green")
        self.grid.blocks[0][2] = Block(color="green")  # Three blocks of the same color
        self.game.select_block(0, 0)
        self.game.select_block(0, 1)
        self.game.select_block(0, 2)  # Select all three
        self.assertEqual(self.score.get_score(), 30, "Score should increase by 30 after clearing three blocks")

    def test_blocks_fall_to_occupy_spaces(self):
        # Functionalities 4: Blocks fall to occupy spaces
        self.grid.blocks[5][5] = Block(color="yellow")
        self.game.clear_blocks([self.grid.blocks[5][5]])  # Clear the block
        self.game.fall_blocks()  # Trigger falling logic
        # Check if the block above falls down (assuming it was yellow)
        self.assertEqual(self.grid.blocks[4][5].get_color(), "yellow", "Block above should fall down to fill the gap")

    def test_undo_last_move(self):
        # Functionalities 5: Undo last move
        self.grid.blocks[1][1] = Block(color="purple")
        self.game.select_block(1, 1)
        self.game.undo_move()  # Undo the selection
        self.assertEqual(len(self.game.move_history), 0, "Move history should be empty after undo")

    def test_save_game_state(self):
        # Functionalities 6: Save game state to a local file
        try:
            self.game.save_game_state()  # This should not raise an error
        except Exception as e:
            self.fail(f"Saving game state raised an exception: {e}")

    def test_load_game_state(self):
        # Functionalities 7: Load game state from a local file
        try:
            self.game.load_game_state()  # This should not raise an error
        except Exception as e:
            self.fail(f"Loading game state raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
