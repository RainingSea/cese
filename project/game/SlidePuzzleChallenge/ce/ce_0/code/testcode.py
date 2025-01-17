import unittest
import os
from game import Game, Tile

class TestSlidePuzzleGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.game.start_game()

    def test_rearrange_tiles(self):
        # Functionalities 1: Slide a tile horizontally into an empty space
        self.game.grid.initialize_grid(4)
        tile_to_slide = self.game.grid.tiles[3][2]  # Assuming this tile can slide into the empty space
        self.game.slide_tile(tile_to_slide)
        self.assertEqual(tile_to_slide.position, (3, 3), "Tile should move to the empty space")

    def test_multiple_difficulty_levels(self):
        # Functionalities 2: Select "Hard" difficulty level
        self.game.difficulty.set_level(4)  # Assuming level 4 is "Hard"
        self.game.start_game()
        self.assertEqual(len(self.game.grid.tiles), 4, "Grid should initialize with 4x4 tiles for hard difficulty")

    def test_timer_functionality(self):
        # Functionalities 3: Start a new game and track time for 10 seconds
        self.game.timer.start()
        time.sleep(10)
        elapsed_time = self.game.timer.get_time()
        self.assertGreaterEqual(elapsed_time, 10, "Timer should track at least 10 seconds")

    def test_save_progress(self):
        # Functionalities 4: Save progress
        self.game.save_progress()
        self.assertTrue(os.path.exists('game_progress.txt'), "Progress should be saved to a file")

    def test_request_hint(self):
        # Functionalities 5: Request hint
        hint = self.game.provide_hint()
        self.assertIn("Try moving the tile", hint, "Hint should suggest a possible move")

    def test_shuffle_tiles(self):
        # Functionalities 6: Shuffle tiles
        initial_state = [tile.number if tile else None for row in self.game.grid.tiles for tile in row]
        self.game.shuffle_tiles()
        shuffled_state = [tile.number if tile else None for row in self.game.grid.tiles for tile in row]
        self.assertNotEqual(initial_state, shuffled_state, "Tiles should be shuffled into a different order")

    def test_confirmation_before_saving(self):
        # Functionalities 7: Confirmation before saving (not implemented in codebase)
        self.fail("Confirmation before saving functionality is not implemented in the codebase")

    def test_reset_puzzle(self):
        # Functionalities 8: Reset puzzle
        self.game.reset_game()
        initial_state = [tile.number if tile else None for row in self.game.grid.tiles for tile in row]
        self.game.shuffle_tiles()
        self.game.reset_game()
        reset_state = [tile.number if tile else None for row in self.game.grid.tiles for tile in row]
        self.assertEqual(initial_state, reset_state, "Puzzle should reset to initial state")

    def test_visual_feedback_on_correct_position(self):
        # Functionalities 9: Visual feedback on correct position (not implemented in codebase)
        self.fail("Visual feedback on correct position functionality is not implemented in the codebase")

    def test_display_current_state_of_the_puzzle(self):
        # Functionalities 10: Display current state of the puzzle
        self.game.start_game()
        current_state = [tile.number if tile else None for row in self.game.grid.tiles for tile in row]
        expected_state = list(range(15)) + [None]
        self.assertEqual(current_state, expected_state, "Puzzle grid should display the current state correctly")

if __name__ == '__main__':
    unittest.main()
