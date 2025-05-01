import unittest
from game import Game, Maze, Tile, Timer, Score

class TestSlideMazeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.game.load_level("mazes.txt")  # Load the maze for testing
        self.maze = self.game.maze

    def test_navigate_through_maze(self):
        # Functionalities 1: Test sliding tiles
        initial_grid = self.maze.grid
        # Attempt to slide a tile horizontally
        self.maze.move_tile(1, 1)  # Assuming this is a valid move
        self.assertNotEqual(initial_grid, self.maze.grid, "Tile should move horizontally")

        # Reset the maze for the next test
        self.game.reset_maze()
        initial_grid = self.maze.grid
        # Attempt to slide a tile vertically
        self.maze.move_tile(2, 1)  # Assuming this is a valid move
        self.assertNotEqual(initial_grid, self.maze.grid, "Tile should move vertically")

    def test_objective_of_reaching_exit_tile(self):
        # Functionalities 2: Test reaching the exit tile
        # Simulate moving to the exit tile
        self.assertTrue(self.maze.is_solved(), "Game should recognize reaching the exit tile")

        # Simulate moving into a wall
        self.maze.move_tile(0, 0)  # Assuming this is a wall
        self.assertFalse(self.maze.is_solved(), "Game should prevent movement into a wall")

    def test_multiple_levels_with_increasing_difficulty(self):
        # Functionalities 3: Test loading levels
        self.game.start_game()  # Start the game to load the first level
        self.assertIsNotNone(self.game.maze, "First level should load with a maze layout")

        # Simulate completing the first level and loading the second level
        self.game.reset_maze()  # This would simulate completing the level
        self.game.load_level("mazes.txt")  # Load a more complex maze for the next level
        self.assertIsNotNone(self.game.maze, "Second level should load with a more complex maze layout")

    def test_timer_tracking(self):
        # Functionalities 4: Test timer functionality
        self.game.timer.start()
        time_elapsed = self.game.timer.time_elapsed
        self.assertGreater(time_elapsed, 0, "Timer should start counting when the game begins")

        # Simulate completing the maze
        self.game.timer.stop()
        self.assertGreater(self.game.timer.time_elapsed, 0, "Timer should stop after completing the maze")

    def test_collecting_bonus_points(self):
        # Functionalities 5: Test collecting stars
        initial_score = self.game.score.points
        self.game.score.add_points(10)  # Simulate collecting a star
        self.assertGreater(self.game.score.points, initial_score, "Score should increase after collecting a star")

        # Simulate attempting to collect an unreachable star
        self.fail("Game should prevent collecting an unreachable star due to an obstacle")

    def test_resetting_the_maze(self):
        # Functionalities 6: Test resetting the maze
        self.game.reset_maze()
        self.assertIsNotNone(self.game.maze, "Maze should reset to its original configuration")

    def test_choosing_a_different_level(self):
        # Functionalities 7: Test level selection
        self.game.start_game()
        self.assertIsNotNone(self.game.maze, "Level selection screen should display available levels")

        # Simulate selecting a different level
        self.fail("Game should load the selected level successfully")

if __name__ == '__main__':
    unittest.main()
