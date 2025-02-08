import unittest
import pygame
from game import Game, Frog, Platform

class TestJumpingFrogGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.frog = self.game.frog
        self.platforms = self.game.platforms

    def test_frog_movement_control(self):
        # Functionalities 1: Test frog movement to the left using left arrow key
        initial_x = self.frog.x
        self.frog.move_left()
        self.assertLess(self.frog.x, initial_x, "Frog should move left")

        # Test frog movement to the right using right arrow key
        initial_x = self.frog.x
        self.frog.move_right()
        self.assertGreater(self.frog.x, initial_x, "Frog should move right")

        # Test frog movement to the left using 'A' key
        initial_x = self.frog.x
        self.frog.move_left()
        self.assertLess(self.frog.x, initial_x, "Frog should move left with 'A' key")

        # Test frog movement to the right using 'D' key
        initial_x = self.frog.x
        self.frog.move_right()
        self.assertGreater(self.frog.x, initial_x, "Frog should move right with 'D' key")

    def test_jumping_mechanism(self):
        # Functionalities 2: Test frog jump
        initial_y = self.frog.y
        self.frog.jump()
        self.assertLess(self.frog.y, initial_y, "Frog should jump upwards")

    def test_platform_movement(self):
        # Functionalities 3: Test platform movement
        platform = self.platforms[0]
        initial_x = platform.x
        platform.move()
        self.assertNotEqual(platform.x, initial_x, "Platform should move horizontally")

    def test_game_over_condition(self):
        # Functionalities 4: Test game over condition (not implemented in codebase)
        self.fail("Game over condition is not implemented in the codebase")

    def test_scoring_system(self):
        # Functionalities 5: Test scoring system (not implemented in codebase)
        self.fail("Scoring system is not implemented in the codebase")

    def test_timer_functionality(self):
        # Functionalities 6: Test timer functionality
        initial_timer = self.game.timer
        self.game.update()
        self.assertGreater(self.game.timer, initial_timer, "Timer should increment over time")

    def test_data_storage(self):
        # Functionalities 7: Test data storage
        self.game.score = 10
        self.game.save_data()
        self.game.score = 0
        self.game.load_data()
        self.assertEqual(self.game.score, 10, "Score should be loaded from the file")

if __name__ == '__main__':
    unittest.main()
