import unittest
from game import Game, Maze, Player, Timer

class TestMazeEscapeChallenge(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.maze = self.game.maze
        self.player = self.game.player
        self.timer = self.game.timer

    def test_maze_generation(self):
        # Functionalities 1: Maze Generation
        self.maze.generate_maze((10, 10))
        self.assertEqual(len(self.maze.grid), 10, "Maze should have 10 rows")
        self.assertEqual(len(self.maze.grid[0]), 10, "Maze should have 10 columns")
        self.assertIn(' ', [cell for row in self.maze.grid for cell in row], "Maze should have pathways")

    def test_player_navigation(self):
        # Functionalities 2: Player Navigation
        initial_position = self.player.get_position()
        self.player.move('up')
        self.assertNotEqual(self.player.get_position(), initial_position, "Player should move up")
        self.player.move('down')
        self.assertNotEqual(self.player.get_position(), initial_position, "Player should move down")
        self.player.move('left')
        self.assertNotEqual(self.player.get_position(), initial_position, "Player should move left")
        self.player.move('right')
        self.assertNotEqual(self.player.get_position(), initial_position, "Player should move right")

    def test_detecting_exit(self):
        # Functionalities 3: Detecting Exit
        self.maze.generate_maze((21, 21))
        self.player.position = (19, 20)  # Assuming this is the exit position
        self.assertTrue(self.game.check_exit(), "Player should detect the exit")

    def test_time_tracking(self):
        # Functionalities 4: Time Tracking
        self.timer.start()
        time.sleep(1)  # Simulate time passing
        elapsed_time = self.timer.get_time()
        self.assertGreater(elapsed_time, 0, "Timer should track time elapsed")

    def test_restart_level(self):
        # Functionalities 5: Restart Level
        self.game.start_game()
        initial_position = self.player.get_position()
        self.player.move('up')
        self.game.restart_level()
        self.assertEqual(self.player.get_position(), initial_position, "Player position should reset after restart")

    def test_return_to_main_menu(self):
        # Functionalities 6: Return to Main Menu (not implemented in codebase)
        self.fail("Return to Main Menu functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
