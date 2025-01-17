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
        # Functionalities 1: Test frog movement to the left
        initial_x = self.frog.x
        self.frog.move_left()
        self.assertLess(self.frog.x, initial_x, "Frog should move left")

        # Test frog movement to the right
        initial_x = self.frog.x
        self.frog.move_right()
        self.assertGreater(self.frog.x, initial_x, "Frog should move right")

    def test_jumping_mechanism(self):
        # Functionalities 2: Test frog jumping upwards
        initial_y = self.frog.y
        self.frog.jump('up', 20)
        self.assertLess(self.frog.y, initial_y, "Frog should jump upwards")

        # Test frog jumping downwards
        initial_y = self.frog.y
        self.frog.jump('down', 20)
        self.assertGreater(self.frog.y, initial_y, "Frog should jump downwards")

    def test_platform_movement(self):
        # Functionalities 3: Test platform movement to the left
        platform = self.platforms[0]
        initial_x = platform.x
        platform.move('left', 10)
        self.assertLess(platform.x, initial_x, "Platform should move left")

        # Test platform movement to the right
        initial_x = platform.x
        platform.move('right', 10)
        self.assertGreater(platform.x, initial_x, "Platform should move right")

    def test_game_over_condition(self):
        # Functionalities 4: Simulate game over condition
        self.game.timer = 0
        self.game.update()
        self.assertLessEqual(self.game.timer, 0, "Game should end when timer reaches zero")

    def test_scoring_system(self):
        # Functionalities 5: Test scoring system
        initial_score = self.game.score
        self.game.check_collision()
        self.assertGreaterEqual(self.game.score, initial_score, "Score should increase on collision")

    def test_timer_functionality(self):
        # Functionalities 6: Test timer decrement
        initial_timer = self.game.timer
        self.game.update()
        self.assertLess(self.game.timer, initial_timer, "Timer should decrease over time")

    def test_data_storage(self):
        # Functionalities 7: Test data storage
        self.game.end_game()
        with open('game_data.txt', 'r') as file:
            data = file.readlines()
        self.assertIn(f'Score: {self.game.score}\n', data, "Score should be saved to file")

if __name__ == '__main__':
    unittest.main()
