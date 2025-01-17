import unittest
import pygame
from game import Game, Tile, Grid, Timer, Difficulty

class TestSlidePuzzleGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()

    def test_rearrange_tiles(self):
        # Functionalities 1: Slide a tile horizontally into an empty space on the grid
        initial_empty_index = next(i for i, tile in enumerate(self.game.grid.tiles) if tile.number == 0)
        tile_to_slide = self.game.grid.tiles[initial_empty_index - 1]
        self.game.slide_tile(tile_to_slide)
        new_empty_index = next(i for i, tile in enumerate(self.game.grid.tiles) if tile.number == 0)
        self.assertEqual(new_empty_index, initial_empty_index - 1, "Tile should move to the empty space")

    def test_multiple_difficulty_levels(self):
        # Functionalities 2: Select "Hard" difficulty level at the start of a new game
        self.game.difficulty.set_level("Hard")
        self.assertEqual(self.game.difficulty.get_level(), "Hard", "Difficulty level should be set to Hard")

    def test_timer_functionality(self):
        # Functionalities 3: Start a new game and track time for 10 seconds
        self.game.timer.start()
        time.sleep(10)
        self.game.timer.stop()
        elapsed_time = self.game.timer.get_elapsed_time()
        self.assertGreaterEqual(elapsed_time, 10, "Timer should track at least 10 seconds")

    def test_save_progress(self):
        # Functionalities 4: Save progress while in-game
        self.game.save_progress()
        with open('progress.txt', 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 3, "Progress file should have 3 lines")

    def test_request_hint(self):
        # Functionalities 5: Request a hint during gameplay
        hint = self.game.provide_hint()
        self.assertEqual(hint, "Hint provided!", "Hint should be provided")

    def test_shuffle_tiles(self):
        # Functionalities 6: Start a new game and observe the initial tile arrangement
        initial_tiles = self.game.grid.tiles[:]
        self.game.shuffle_tiles()
        self.assertNotEqual(initial_tiles, self.game.grid.tiles, "Tiles should be shuffled")

    def test_confirmation_before_saving(self):
        # Functionalities 7: Confirmation before saving (not implemented in codebase)
        self.fail("Confirmation before saving is not implemented in the codebase")

    def test_reset_puzzle(self):
        # Functionalities 8: Reset the puzzle while in-game
        self.game.reset_game()
        self.assertEqual(len(self.game.grid.tiles), 16, "Game should reset with 16 tiles")

    def test_visual_feedback_on_correct_position(self):
        # Functionalities 9: Visual feedback on correct position (not implemented in codebase)
        self.fail("Visual feedback on correct position is not implemented in the codebase")

    def test_display_current_state_of_the_puzzle(self):
        # Functionalities 10: Display current state of the puzzle
        self.assertIsInstance(self.game.grid, Grid, "Grid should be displayed correctly")

if __name__ == '__main__':
    unittest.main()
