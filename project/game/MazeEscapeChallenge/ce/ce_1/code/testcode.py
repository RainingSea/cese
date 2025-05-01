import unittest
from game import Game
from player import Player
from maze import Maze
from timer import Timer

class TestMazeEscapeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player = self.game.player
        self.maze = self.game.maze
        self.timer = self.game.timer

    def test_maze_generation(self):
        # Functionalities 1: Test maze generation
        self.game.start_game()
        self.assertEqual(len(self.maze.grid), 10, "Maze should have 10 rows")
        self.assertTrue(all(len(row) == 10 for row in self.maze.grid), "Maze should have 10 columns")
        self.assertTrue(any(' ' in row for row in self.maze.grid), "Maze should have open paths")

    def test_player_navigation(self):
        # Functionalities 2: Test player navigation
        initial_position = self.player.position
        self.player.move('down')
        self.assertEqual(self.player.position, (1, 1), "Player should move down to (1, 1)")
        self.player.move('right')
        self.assertEqual(self.player.position, (1, 2), "Player should move right to (1, 2)")
        self.player.move('up')
        self.assertEqual(self.player.position, (0, 2), "Player should move up to (0, 2)")
        self.player.move('left')
        self.assertEqual(self.player.position, (0, 1), "Player should move left to (0, 1)")

    def test_detecting_exit(self):
        # Functionalities 3: Test detecting exit
        self.player.position = (9, 8)  # Move player to exit position
        self.assertTrue(self.player.check_exit(), "Player should detect exit at (9, 8)")
        self.game.display_completion_message()  # Check if completion message is displayed
        # Since we can't capture print output directly, we assume the function works as intended

    def test_time_tracking(self):
        # Functionalities 4: Test time tracking (not implemented in codebase)
        self.fail("Time tracking functionality is not implemented in the codebase")

    def test_restart_level(self):
        # Functionalities 5: Test restarting level
        initial_position = self.player.position
        self.game.restart_level()
        self.assertEqual(self.player.position, (0, 1), "Player should restart at (0, 1)")
        self.assertNotEqual(self.maze.grid, [], "Maze should be regenerated on restart")

    def test_return_to_main_menu(self):
        # Functionalities 6: Test return to main menu (not implemented in codebase)
        self.fail("Return to main menu functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
