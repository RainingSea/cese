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
        # Functionalities 2: Test frog jumping onto a platform
        self.frog.y = self.platforms[0].y - 30
        initial_y = self.frog.y
        self.frog.jump()
        self.assertLess(self.frog.y, initial_y, "Frog should jump upwards")

        # Test frog jumping off a platform
        self.frog.y = self.platforms[0].y - 30
        self.frog.jump()
        self.assertNotEqual(self.frog.y, self.platforms[0].y - 30, "Frog should not land on the same platform")

    def test_platform_movement(self):
        # Functionalities 3: Test platform movement (not implemented in codebase)
        self.fail("Platform movement functionality is not implemented in the codebase")

    def test_game_over_condition(self):
        # Functionalities 4: Test game over when frog falls into water
        self.game.timer = 0
        self.game.end_game()
        self.assertFalse(pygame.get_init(), "Game should end when timer reaches zero")

    def test_scoring_system(self):
        # Functionalities 5: Test scoring system (not implemented in codebase)
        self.fail("Scoring system functionality is not implemented in the codebase")

    def test_timer_functionality(self):
        # Functionalities 6: Test timer functionality (not implemented in codebase)
        self.fail("Timer functionality is not implemented in the codebase")

    def test_data_storage(self):
        # Functionalities 7: Test data storage after game session
        self.game.save_score()
        with open('game_data.txt', 'r') as f:
            data = f.read()
        self.assertIn(f'Score: {self.game.score}', data, "Score should be saved to the file")

if __name__ == '__main__':
    unittest.main()
