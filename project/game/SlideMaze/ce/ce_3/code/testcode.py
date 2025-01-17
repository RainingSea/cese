import unittest
from game import Game
from maze import Maze
from player import Player
from timer import Timer

class TestSlideMazeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.maze = self.game.maze
        self.player = self.game.player
        self.timer = self.game.timer

    def test_navigate_through_maze(self):
        # Functionality 1: Navigate Through the Maze
        self.game.start_game()
        initial_layout = self.maze.tiles.copy()

        # Attempt to slide a tile horizontally
        moved_horizontally = self.maze.move_tile('horizontal')
        self.assertTrue(moved_horizontally, "Tile should move horizontally")
        self.assertNotEqual(self.maze.tiles, initial_layout, "Maze layout should update after horizontal move")

        # Attempt to slide a tile vertically
        moved_vertically = self.maze.move_tile('vertical')
        self.assertTrue(moved_vertically, "Tile should move vertically")
        self.assertNotEqual(self.maze.tiles, initial_layout, "Maze layout should update after vertical move")

    def test_objective_of_reaching_exit_tile(self):
        # Functionality 2: Objective of Reaching the Exit Tile
        self.game.start_game()
        self.player.position = (1, 1)  # Assume starting position

        # Move player to exit tile
        self.player.move('exit')
        self.assertTrue(self.maze.is_solved(), "Player should reach the exit tile")

        # Attempt to move into a wall
        self.player.move('wall')
        self.assertNotEqual(self.player.position, (1, 1), "Player should not move into a wall")

    def test_multiple_levels_with_increasing_difficulty(self):
        # Functionality 3: Multiple Levels with Increasing Difficulty
        self.game.start_game()
        self.assertEqual(self.maze.tiles, self.game.read_maze_from_file(1), "First level should load correctly")

        # Simulate completing the first level and loading the second
        self.game.load_maze(2)
        self.assertEqual(self.maze.tiles, self.game.read_maze_from_file(2), "Second level should load correctly")

    def test_timer_tracking(self):
        # Functionality 4: Timer Tracking
        self.game.start_game()
        self.timer.start()
        initial_time = self.timer.elapsed_time()

        # Simulate some time passing
        self.assertGreater(self.timer.elapsed_time(), initial_time, "Timer should track elapsed time")

    def test_collecting_bonus_points(self):
        # Functionality 5: Collecting Bonus Points
        self.game.start_game()
        initial_score = self.player.score

        # Simulate collecting a star
        self.player.collect_star()
        self.assertGreater(self.player.score, initial_score, "Player score should increase after collecting a star")

        # Attempt to collect an unreachable star
        self.fail("Unreachable star collection logic is not implemented in the codebase")

    def test_resetting_the_maze(self):
        # Functionality 6: Resetting the Maze
        self.game.start_game()
        self.game.reset_maze()
        self.assertEqual(self.maze.tiles, self.game.read_maze_from_file(1), "Maze should reset to original configuration")

        # Attempt to reset after reaching the exit
        self.fail("Reset after reaching exit logic is not implemented in the codebase")

    def test_choosing_a_different_level(self):
        # Functionality 7: Choosing a Different Level
        self.game.start_game()
        self.game.load_maze(2)
        self.assertEqual(self.maze.tiles, self.game.read_maze_from_file(2), "Selected level should load correctly")

if __name__ == '__main__':
    unittest.main()
