import unittest
from game import Game, Tile, Grid, Timer, Settings

class TestSlidePuzzleGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.grid = self.game.grid
        self.timer = self.game.timer
        self.settings = self.game.settings

    def test_rearrange_tiles(self):
        # Functionalities 1: Slide a tile horizontally into an empty space on the grid
        initial_tiles = self.grid.tiles[:]
        empty_index = initial_tiles.index(Tile(0))
        # Find a tile adjacent to the empty space
        adjacent_index = empty_index + 1 if empty_index % self.grid.size != self.grid.size - 1 else empty_index - 1
        tile_to_slide = initial_tiles[adjacent_index]
        self.grid.slide_tile(tile_to_slide)
        self.assertNotEqual(self.grid.tiles, initial_tiles, "Tile should move to the empty space")

    def test_multiple_difficulty_levels(self):
        # Functionalities 2: Select "Hard" difficulty level at the start of a new game
        self.game.start_game(difficulty='hard')
        self.assertEqual(self.settings.difficulty, 'hard', "Game should start with 'hard' difficulty")

    def test_timer_functionality(self):
        # Functionalities 3: Start a new game and track time for 10 seconds
        self.timer.start_timer()
        time.sleep(10)
        elapsed_time = self.timer.stop_timer()
        self.assertGreaterEqual(elapsed_time, 10, "Timer should track at least 10 seconds")

    def test_save_progress(self):
        # Functionalities 4: Save progress while in-game
        self.game.save_progress()
        with open('game_state.txt', 'r') as file:
            lines = file.readlines()
            self.assertEqual(len(lines), 2, "Game state should be saved with 2 lines of data")

    def test_request_hint(self):
        # Functionalities 5: Request a hint during gameplay
        hint = self.game.provide_hint()
        self.assertIsInstance(hint, str, "Hint should be a string")

    def test_shuffle_tiles(self):
        # Functionalities 6: Start a new game and observe the initial tile arrangement
        initial_tiles = self.grid.tiles[:]
        self.grid.shuffle_tiles()
        self.assertNotEqual(self.grid.tiles, initial_tiles, "Tiles should be shuffled into a new order")

    def test_confirmation_before_saving(self):
        # Functionalities 7: Attempt to save progress and click "Cancel"
        # This functionality is not implemented in the codebase
        self.fail("Confirmation before saving is not implemented in the codebase")

    def test_reset_puzzle(self):
        # Functionalities 8: Reset the puzzle while in-game
        self.game.reset_game()
        self.assertEqual(self.grid.tiles[-1].value, 0, "Puzzle should reset with the empty tile in the last position")

    def test_visual_feedback_on_correct_position(self):
        # Functionalities 9: Slide a tile into its correct position
        # This functionality is not implemented in the codebase
        self.fail("Visual feedback on correct position is not implemented in the codebase")

    def test_display_current_state_of_the_puzzle(self):
        # Functionalities 10: Start a new game and view the puzzle grid
        self.assertIsInstance(self.grid.tiles, list, "Puzzle grid should be displayed as a list of tiles")

if __name__ == '__main__':
    unittest.main()
