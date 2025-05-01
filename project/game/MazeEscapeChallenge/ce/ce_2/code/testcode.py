import unittest
from game import Game

class TestMazeEscapeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_maze_generation(self):
        # Functionalities 1: Test maze generation
        self.game.start_game()
        self.assertEqual(len(self.game.maze.grid), 10, "Maze should have 10 rows")
        self.assertTrue(all(len(row) == 10 for row in self.game.maze.grid), "Maze should have 10 columns")
        self.assertTrue(any(' ' in row for row in self.game.maze.grid), "Maze should contain pathways")

    def test_player_navigation(self):
        # Functionalities 2: Test player navigation
        initial_position = self.game.player.position.copy()
        self.game.player.move('UP')
        self.assertEqual(self.game.player.position, [initial_position[0], initial_position[1] - 1], "Player should move up")
        
        self.game.player.move('DOWN')
        self.assertEqual(self.game.player.position, initial_position, "Player should move back down to original position")
        
        self.game.player.move('LEFT')
        self.assertEqual(self.game.player.position, [initial_position[0] - 1, initial_position[1]], "Player should move left")
        
        self.game.player.move('RIGHT')
        self.assertEqual(self.game.player.position, initial_position, "Player should move back to original position")

    def test_detecting_exit(self):
        # Functionalities 3: Test detecting exit
        self.game.player.position = self.game.exit_position
        self.assertTrue(self.game.player.check_exit(self.game.exit_position), "Player should detect exit at exit position")
        
        self.game.player.position = [0, 0]  # Move player away from exit
        self.assertFalse(self.game.player.check_exit(self.game.exit_position), "Player should not detect exit at a different position")

    def test_time_tracking(self):
        # Functionalities 4: Test time tracking (not implemented in codebase)
        self.fail("Time tracking functionality is not implemented in the codebase")

    def test_restart_level(self):
        # Functionalities 5: Test restarting level
        initial_position = self.game.player.position.copy()
        self.game.player.move('UP')  # Move player
        self.game.restart_level()
        self.assertEqual(self.game.player.position, [1, 1], "Player position should reset to starting position after restart")

    def test_return_to_main_menu(self):
        # Functionalities 6: Test return to main menu (not implemented in codebase)
        self.fail("Return to main menu functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
