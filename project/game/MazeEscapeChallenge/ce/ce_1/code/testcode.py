import unittest
from maze import Maze
from player import Player
from game import Game
import time

class TestMazeEscapeChallenge(unittest.TestCase):

    def test_maze_generation(self):
        # Functionalities 1: Maze Generation
        maze = Maze(10, 10)
        self.assertEqual(len(maze.grid), 10, "Maze height should be 10")
        self.assertEqual(len(maze.grid[0]), 10, "Maze width should be 10")
        self.assertIn(' ', maze.grid[1], "Maze should have pathways")

    def test_player_navigation(self):
        # Functionalities 2: Player Navigation
        player = Player((1, 1))
        player.move('right')
        self.assertEqual(player.position, (1, 2), "Player should move right to (1, 2)")
        player.move('down')
        self.assertEqual(player.position, (2, 2), "Player should move down to (2, 2)")
        player.move('left')
        self.assertEqual(player.position, (2, 1), "Player should move left to (2, 1)")
        player.move('up')
        self.assertEqual(player.position, (1, 1), "Player should move up to (1, 1)")

    def test_detecting_exit(self):
        # Functionalities 3: Detecting Exit
        player = Player((1, 1))
        player.start_time = time.time()
        player.reach_exit()
        self.assertGreater(player.completion_time, 0, "Completion time should be greater than 0")

    def test_time_tracking(self):
        # Functionalities 4: Time Tracking
        player = Player((1, 1))
        player.start_time = time.time()
        time.sleep(1)  # Simulate time taken to complete the maze
        player.reach_exit()
        self.assertAlmostEqual(player.completion_time, 1, delta=0.1, msg="Completion time should be approximately 1 second")

    def test_restart_level(self):
        # Functionalities 5: Restart Level
        maze = Maze(21, 21)
        player = Player((5, 5))
        game = Game(maze, player)
        game.restart_level()
        self.assertEqual(player.position, (1, 1), "Player position should reset to (1, 1)")

    def test_return_to_main_menu(self):
        # Functionalities 6: Return to Main Menu (not implemented in codebase)
        self.fail("Return to main menu functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
