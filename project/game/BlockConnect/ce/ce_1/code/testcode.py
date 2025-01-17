import unittest
import os
from game import Game

class TestBlockConnectGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_select_and_connect_blocks(self):
        # Functionalities 1: Select and Connect Blocks of the Same Color
        self.game.select_block(0, 0)
        self.game.select_block(0, 1)
        self.assertEqual(self.game.grid[0][0], 1, "Block at (0, 0) should be selected")
        self.assertEqual(self.game.grid[0][1], 1, "Block at (0, 1) should be selected")
        self.game.clear_blocks([(0, 0), (0, 1)])
        self.assertEqual(self.game.grid[0][0], 0, "Block at (0, 0) should be cleared")
        self.assertEqual(self.game.grid[0][1], 0, "Block at (0, 1) should be cleared")

    def test_display_game_grid(self):
        # Functionalities 2: Display the Game Grid
        # This functionality is visual and cannot be directly tested with assertions
        # However, we can ensure no exceptions are raised during grid drawing
        try:
            self.game.draw_grid()
        except Exception as e:
            self.fail(f"Drawing grid raised an exception: {e}")

    def test_score_calculation_after_block_clearing(self):
        # Functionalities 3: Score Calculation After Block Clearing
        initial_score = self.game.score
        self.game.clear_blocks([(0, 0), (0, 1), (0, 2)])
        self.assertEqual(self.game.score, initial_score + 3, "Score should increase by 3")

    def test_blocks_fall_to_occupy_spaces(self):
        # Functionalities 4: Blocks Fall to Occupy Spaces
        self.game.grid[9][0] = 1
        self.game.grid[8][0] = 1
        self.game.clear_blocks([(9, 0)])
        self.game.fall_blocks()
        self.assertEqual(self.game.grid[9][0], 1, "Block should fall to the bottom")
        self.assertEqual(self.game.grid[8][0], 0, "Space above should be empty")

    def test_undo_last_move(self):
        # Functionalities 5: Undo Last Move
        self.game.select_block(0, 0)
        self.game.undo_move()
        self.assertEqual(self.game.grid[0][0], 0, "Block at (0, 0) should be reverted")

    def test_save_game_state(self):
        # Functionalities 6: Save Game State to a Local File
        self.game.save_game_state()
        self.assertTrue(os.path.exists('game_state.txt'), "Game state file should exist")

    def test_load_game_state(self):
        # Functionalities 7: Load Game State from a Local File
        self.game.score = 10
        self.game.save_game_state()
        self.game.score = 0
        self.game.load_game_state()
        self.assertEqual(self.game.score, 10, "Game score should be restored to 10")

if __name__ == '__main__':
    unittest.main()
