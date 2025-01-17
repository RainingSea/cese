import unittest
import json
from game import Game

class TestBlockConnectGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_select_and_connect_blocks(self):
        # Functionalities 1: Select and Connect Blocks of the Same Color
        self.game.grid = [
            ['red', 'red', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', '']
        ]
        self.game.connect_blocks([(0, 0), (0, 1)])
        self.assertEqual(self.game.grid[0][0], 'red', "Blocks should be connected with the same color")
        self.assertEqual(self.game.grid[0][1], 'red', "Blocks should be connected with the same color")

    def test_display_game_grid(self):
        # Functionalities 2: Display the Game Grid
        # Since display_grid only prints, we will check if the method runs without error
        try:
            self.game.display_grid()
        except Exception as e:
            self.fail(f"display_grid method raised an exception: {e}")

    def test_score_calculation_after_block_clearing(self):
        # Functionalities 3: Score Calculation After Block Clearing
        initial_score = self.game.score
        self.game.connect_blocks([(0, 0), (0, 1), (0, 2)])
        self.assertEqual(self.game.score, initial_score + 3, "Score should increase by the number of blocks cleared")

    def test_blocks_fall_to_occupy_spaces(self):
        # Functionalities 4: Blocks Fall to Occupy Spaces
        # This functionality is not implemented in the codebase
        self.fail("Blocks falling to occupy spaces functionality is not implemented in the codebase")

    def test_undo_last_move(self):
        # Functionalities 5: Undo Last Move
        self.game.grid = [
            ['red', 'red', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', '']
        ]
        self.game.history.append([['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']])
        self.game.undo_move()
        self.assertEqual(self.game.grid, [['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']], "Undo should revert the grid to the previous state")

    def test_save_game_state(self):
        # Functionalities 6: Save Game State to a Local File
        self.game.save_game_state()
        try:
            with open('game_state.txt', 'r') as f:
                data = json.load(f)
                self.assertIn('grid', data, "Saved game state should contain grid")
                self.assertIn('score', data, "Saved game state should contain score")
        except Exception as e:
            self.fail(f"Saving game state raised an exception: {e}")

    def test_load_game_state(self):
        # Functionalities 7: Load Game State from a Local File
        self.game.load_game_state()
        expected_grid = [
            ["red", "blue", "green", "yellow", "blue"],
            ["blue", "green", "red", "yellow", "green"],
            ["yellow", "red", "blue", "green", "red"],
            ["green", "yellow", "blue", "red", "blue"],
            ["red", "green", "yellow", "blue", "green"]
        ]
        self.assertEqual(self.game.grid, expected_grid, "Loaded game state should match the saved grid")
        self.assertEqual(self.game.score, 250, "Loaded game state should match the saved score")

if __name__ == '__main__':
    unittest.main()
