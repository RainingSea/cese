import unittest
import pygame
from game import Game
from player import Player
from maze import Maze
from timer import Timer

class TestMazeEscapeChallenge(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player = self.game.player
        self.maze = self.game.maze
        self.timer = self.game.timer

    def test_maze_generation(self):
        # Functionalities 1: Maze Generation
        self.game.start_game()
        self.assertEqual(len(self.maze.grid), 10, "Maze should be generated with size 10x10")
        self.assertEqual(len(self.maze.grid[0]), 10, "Maze should be generated with size 10x10")
        self.assertIn(' ', [cell for row in self.maze.grid for cell in row], "Maze should contain pathways")

    def test_player_navigation(self):
        # Functionalities 2: Player Navigation
        initial_position = self.player.get_position()
        self.game.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT}))
        self.assertNotEqual(self.player.get_position(), initial_position, "Player should move right")
        self.game.handle_input(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}))
        self.assertNotEqual(self.player.get_position(), initial_position, "Player should move down")

    def test_detecting_exit(self):
        # Functionalities 3: Detecting Exit
        self.player.position = (9, 9)  # Move player to the exit position
        self.assertTrue(self.game.check_exit(), "Game should detect when the exit is reached")

    def test_time_tracking(self):
        # Functionalities 4: Time Tracking
        self.timer.start()
        pygame.time.delay(1000)  # Simulate 1 second delay
        elapsed_time = self.timer.get_elapsed_time()
        self.assertAlmostEqual(elapsed_time, 1, delta=0.1, msg="Timer should track time accurately")

    def test_restart_level(self):
        # Functionalities 5: Restart Level
        self.player.position = (5, 5)  # Change player position
        self.game.restart_game()
        self.assertEqual(self.player.get_position(), (0, 0), "Player position should reset to start")
        self.assertEqual(len(self.maze.grid), 10, "Maze should be regenerated with size 10x10")

    def test_return_to_main_menu(self):
        # Functionalities 6: Return to Main Menu (not implemented in codebase)
        self.fail("Return to main menu functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
