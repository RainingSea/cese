import unittest
from maze import Maze
from player import Player
from game import Game

class TestMazeEscapeChallenge(unittest.TestCase):

    def setUp(self):
        # Initialize the maze and player for testing
        self.maze = Maze(10, 10)
        self.player = Player((1, 0))
        self.game = Game(self.maze, self.player)

    def test_maze_generation(self):
        # Functionalities 1: Maze Generation
        self.assertEqual(len(self.maze.grid), 10, "Maze height should be 10")
        self.assertEqual(len(self.maze.grid[0]), 10, "Maze width should be 10")
        self.assertIn(' ', [cell for row in self.maze.grid for cell in row], "Maze should contain pathways")

    def test_player_navigation(self):
        # Functionalities 2: Player Navigation
        initial_position = self.player.position
        self.player.move('right')
        self.assertNotEqual(self.player.position, initial_position, "Player should move right")
        self.player.move('down')
        self.assertNotEqual(self.player.position, initial_position, "Player should move down")

    def test_detecting_exit(self):
        # Functionalities 3: Detecting Exit
        self.player.position = (self.maze.height - 2, self.maze.width - 1)
        self.assertTrue(self.game.check_exit(), "Player should be at the exit")

    def test_time_tracking(self):
        # Functionalities 4: Time Tracking
        self.game.start_time = 0
        self.player.set_time(10.0)
        self.assertEqual(self.player.time_taken, 10.0, "Time taken should be tracked accurately")

    def test_restart_level(self):
        # Functionalities 5: Restart Level (not implemented in codebase)
        self.fail("Restart level functionality is not implemented in the codebase")

    def test_return_to_main_menu(self):
        # Functionalities 6: Return to Main Menu (not implemented in codebase)
        self.fail("Return to main menu functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
