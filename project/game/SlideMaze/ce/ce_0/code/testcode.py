import unittest
from game import Game, Maze, Player, Timer, Score

class TestSlideMazeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.game.load_maze(0)  # Load the first maze
        self.player = self.game.player
        self.maze = self.game.maze
        self.timer = self.game.timer
        self.score = self.game.score

    def test_navigate_through_maze(self):
        # Functionality 1: Navigate Through the Maze
        # Test horizontal tile movement
        self.assertTrue(self.maze.move_tile('right'), "Tile should move horizontally")
        # Test vertical tile movement
        self.assertTrue(self.maze.move_tile('down'), "Tile should move vertically")

    def test_objective_of_reaching_exit_tile(self):
        # Functionality 2: Objective of Reaching the Exit Tile
        # Move player to exit tile
        self.player.move('right')
        self.player.move('down')
        self.assertEqual(self.player.get_position(), (1, 1), "Player should reach the exit tile")
        # Attempt to move into a wall
        self.player.move('left')
        self.assertEqual(self.player.get_position(), (1, 1), "Player should not move into a wall")

    def test_multiple_levels_with_increasing_difficulty(self):
        # Functionality 3: Multiple Levels with Increasing Difficulty
        # Load first level
        self.game.load_maze(0)
        self.assertIsNotNone(self.game.maze, "First level should load")
        # Simulate completing first level and loading second
        self.game.load_maze(1)
        self.assertIsNotNone(self.game.maze, "Second level should load")

    def test_timer_tracking(self):
        # Functionality 4: Timer Tracking
        self.timer.start()
        self.assertGreater(self.timer.get_elapsed_time(), 0, "Timer should start counting")
        # Simulate completing the maze
        self.timer.start_time = None  # Reset timer for test
        self.assertEqual(self.timer.get_elapsed_time(), 0, "Timer should stop after completion")

    def test_collecting_bonus_points(self):
        # Functionality 5: Collecting Bonus Points
        self.score.add_points(10)
        self.assertEqual(self.score.get_score(), 10, "Score should increase by bonus points")
        # Attempt to collect unreachable star
        self.fail("Collecting unreachable star functionality is not implemented in the codebase")

    def test_resetting_the_maze(self):
        # Functionality 6: Resetting the Maze
        self.game.reset_maze()
        self.assertEqual(self.player.get_position(), (0, 0), "Player should return to starting point")
        # Reset after reaching exit
        self.game.reset_maze()
        self.assertEqual(self.player.get_position(), (0, 0), "Maze should reset successfully")

    def test_choosing_a_different_level(self):
        # Functionality 7: Choosing a Different Level
        self.game.load_maze(0)
        self.assertIsNotNone(self.game.maze, "First level should load")
        # Simulate selecting a different level
        self.game.load_maze(1)
        self.assertIsNotNone(self.game.maze, "Different level should load successfully")

if __name__ == '__main__':
    unittest.main()
