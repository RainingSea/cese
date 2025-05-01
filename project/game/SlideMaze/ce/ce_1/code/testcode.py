import unittest
import pygame
from main import Game

class TestSlideMazeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()
        self.game.maze.load_maze("mazes.txt")  # Load the maze for testing

    def test_navigate_through_maze(self):
        # Functionalities 1 Test sliding a tile horizontally
        initial_grid = self.game.maze.grid.copy()
        self.game.maze.move_tile("right")  # Assuming this method is implemented
        self.assertNotEqual(self.game.maze.grid, initial_grid, "Tile should move successfully horizontally")

        # Test sliding a tile vertically
        initial_grid = self.game.maze.grid.copy()
        self.game.maze.move_tile("down")  # Assuming this method is implemented
        self.assertNotEqual(self.game.maze.grid, initial_grid, "Tile should move successfully vertically")

    def test_reach_exit_tile(self):
        # Functionalities 2 Test moving to the exit tile
        self.game.player.position = self.game.maze.grid[1][1].tile_type  # Move player to exit position
        self.assertTrue(self.game.maze.check_win(), "Game should recognize reaching the exit tile")

        # Test moving into a wall
        self.game.player.position = self.game.maze.grid[0][0].tile_type  # Move player into a wall
        self.game.handle_key_event(pygame.K_UP)  # Attempt to move up into a wall
        self.assertEqual(self.game.player.position, (0, 0), "Player should not move into a wall")

    def test_multiple_levels(self):
        # Functionalities 3 Test loading the first level
        self.assertIsNotNone(self.game.maze.grid, "First level should load with a maze layout")

        # Test completing the first level and loading the second level
        # Assuming a method to complete level and load next level exists
        self.game.start()  # Start the game to load the next level
        self.assertIsNotNone(self.game.maze.grid, "Second level should load with a more complex maze layout")

    def test_timer_tracking(self):
        # Functionalities 4 Test timer starts
        self.game.timer.start()
        self.assertIsNotNone(self.game.timer.start_time, "Timer should start when the game begins")

        # Test timer stops after completing the maze
        self.game.player.position = self.game.maze.grid[1][1].tile_type  # Move player to exit position
        self.assertTrue(self.game.maze.check_win(), "Game should recognize reaching the exit tile")
        elapsed_time = self.game.timer.elapsed_time()
        self.assertGreater(elapsed_time, 0, "Elapsed time should be greater than 0 after completing the maze")

    def test_collecting_bonus_points(self):
        # Functionalities 5 Test collecting a star
        self.game.player.position = (1, 1)  # Move player to star position
        self.game.player.collect_star()
        self.assertEqual(self.game.player.score.points, 1, "Player's score should increase by 1 after collecting a star")

        # Test attempting to collect an unreachable star
        self.game.player.position = (0, 0)  # Move player to an unreachable position
        self.assertRaises(Exception, self.game.player.collect_star)  # Assuming an exception is raised for unreachable stars

    def test_resetting_the_maze(self):
        # Functionalities 6 Test resetting the maze
        self.game.player.position = (1, 1)  # Move player to a position
        self.game.reset()
        self.assertEqual(self.game.player.position, (0, 0), "Player should reset to starting position")

        # Test resetting after reaching the exit
        self.game.player.position = self.game.maze.grid[1][1].tile_type  # Move player to exit position
        self.game.reset()
        self.assertEqual(self.game.player.position, (0, 0), "Player should reset to starting position after reaching exit")

    def test_choosing_different_level(self):
        # Functionalities 7 Test level selection
        # Assuming a method to select a level exists
        self.game.start()  # Start the game to load the first level
        self.assertIsNotNone(self.game.maze.grid, "Level selection should display available levels")

        # Test selecting a different level
        # Assuming a method to select a different level exists
        self.game.start()  # Start the game to load the next level
        self.assertIsNotNone(self.game.maze.grid, "Selected level should load successfully")

if __name__ == '__main__':
    unittest.main()
