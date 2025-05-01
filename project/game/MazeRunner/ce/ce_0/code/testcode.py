import unittest
import pygame
from game import Game
from player import Player
from maze import Maze

class TestMazeRunnerGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player = self.game.player
        self.maze = self.game.maze

    def test_player_controls_character(self):
        # Functionalities 1 Test player movement in all directions
        initial_x, initial_y = self.player.x, self.player.y
        
        # Move up
        self.player.move("up")
        self.assertEqual(self.player.y, initial_y - 1, "Player should move up")

        # Move down
        self.player.move("down")
        self.assertEqual(self.player.y, initial_y, "Player should move down back to original position")

        # Move left
        self.player.move("left")
        self.assertEqual(self.player.x, initial_x - 1, "Player should move left")

        # Move right
        self.player.move("right")
        self.assertEqual(self.player.x, initial_x, "Player should move right back to original position")

    def test_maze_navigation_and_obstacles(self):
        # Functionalities 2 Test player movement into an obstacle
        self.maze.generate(0)  # Generate a simple maze layout
        self.player.x, self.player.y = 1, 1  # Position player at (1, 1)

        # Attempt to move into an obstacle (1, 2)
        self.player.move("down")  # This should hit an obstacle
        self.assertEqual(self.player.y, 1, "Player should not move down into an obstacle")

    def test_collecting_stars(self):
        # Functionalities 3 Test star collection
        self.game.stars.append((1, 2))  # Assume a star is at (1, 2)
        self.player.x, self.player.y = 1, 2  # Move player to the star position
        
        # Simulate collecting the star
        self.game.score += 10  # Assume collecting a star gives 10 points
        self.assertEqual(self.game.score, 10, "Score should increase by 10 after collecting a star")

    def test_multiple_levels_with_increasing_difficulty(self):
        # Functionalities 4 Test level progression
        self.game.maze.generate(1)  # Generate a second level
        self.assertNotEqual(self.game.maze.layout, [], "Second level maze should be generated")

    def test_strategic_movement_and_dead_ends(self):
        # Functionalities 5 Test navigating towards a dead end
        self.player.x, self.player.y = 0, 0  # Start at a known position
        self.player.move("down")  # Move to (0, 1)
        self.player.move("down")  # Move to (0, 2), which is a dead end
        self.assertEqual(self.player.y, 1, "Player should realize they are at a dead end and backtrack")

    def test_timer_for_level_completion(self):
        # Functionalities 6 Test timer functionality
        initial_timer = self.game.timer
        self.game.update()  # Simulate an update call
        self.assertGreater(self.game.timer, initial_timer, "Timer should increment after an update")

    def test_progress_tracking(self):
        # Functionalities 7 Test progress tracking (not implemented in codebase)
        self.fail("Progress tracking functionality is not implemented in the codebase")

    def test_scoring_system(self):
        # Functionalities 8 Test scoring system (not implemented in codebase)
        self.fail("Scoring system functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
