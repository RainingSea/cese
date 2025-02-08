import unittest
from game import Game
from maze import Maze
from player import Player
from timer import Timer

class TestMazeEscapeChallenge(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.maze = self.game.maze
        self.player = self.game.player
        self.timer = self.game.timer

    def test_maze_generation(self):
        # Functionalities 1: Maze Generation
        self.maze.generate_maze(10)
        self.assertEqual(len(self.maze.walls), 10, "Maze should have 10 rows")
        self.assertEqual(len(self.maze.walls[0]), 10, "Maze should have 10 columns")
        self.assertTrue(any(cell == 0 for row in self.maze.walls for cell in row), "Maze should have pathways")

    def test_player_navigation(self):
        # Functionalities 2: Player Navigation
        initial_x, initial_y = self.player.position_x, self.player.position_y
        self.player.move('right')
        self.assertEqual(self.player.position_x, initial_x + 1, "Player should move right")
        self.player.move('down')
        self.assertEqual(self.player.position_y, initial_y + 1, "Player should move down")
        self.player.move('left')
        self.assertEqual(self.player.position_x, initial_x, "Player should move left")
        self.player.move('up')
        self.assertEqual(self.player.position_y, initial_y, "Player should move up")

    def test_detecting_exit(self):
        # Functionalities 3: Detecting Exit
        self.maze.generate_maze(10)
        self.player.position_x, self.player.position_y = 9, 9  # Assuming exit is at bottom-right
        self.assertTrue(self.player.check_exit(self.maze), "Player should detect exit")

    def test_time_tracking(self):
        # Functionalities 4: Time Tracking
        self.timer.start()
        self.timer.stop()
        self.assertGreaterEqual(self.timer.get_time(), 0, "Timer should track time accurately")

    def test_restart_level(self):
        # Functionalities 5: Restart Level
        self.player.position_x, self.player.position_y = 5, 5
        self.game.restart_level()
        self.assertEqual(self.player.position_x, 0, "Player position should reset to start")
        self.assertEqual(self.player.position_y, 0, "Player position should reset to start")

    def test_return_to_main_menu(self):
        # Functionalities 6: Return to Main Menu (not implemented in codebase)
        self.fail("Return to main menu functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
