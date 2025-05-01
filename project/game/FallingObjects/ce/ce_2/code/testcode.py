import unittest
import pygame
from game import Game

class TestFallingObjectsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.basket = self.game.basket
        self.falling_objects = self.game.falling_objects

    def test_basket_initial_position(self):
        # Functionality 1: Check initial position of the basket
        self.assertEqual(self.basket.position, self.game.screen_width // 2, "Basket should be at the bottom center of the screen")

    def test_basket_movement(self):
        # Functionality 1: Test basket movement to the left
        initial_position = self.basket.position
        self.basket.move_left()
        self.assertLess(self.basket.position, initial_position, "Basket should move left")

        # Test basket movement to the right
        initial_position = self.basket.position
        self.basket.move_right()
        self.assertGreater(self.basket.position, initial_position, "Basket should move right")

        # Test basket does not move off the screen to the left
        self.basket.position = 0
        self.basket.move_left()
        self.assertEqual(self.basket.position, 0, "Basket should not move off the screen to the left")

        # Test basket does not move off the screen to the right
        self.basket.position = self.game.screen_width - self.basket.width
        self.basket.move_right()
        self.assertEqual(self.basket.position, self.game.screen_width - self.basket.width, "Basket should not move off the screen to the right")

    def test_catching_falling_objects(self):
        # Functionality 2: Catching falling objects
        self.falling_objects.append(FallingObject(self.basket.position + 10, 0))  # Position it directly above the basket
        initial_score = self.game.score
        self.basket.position = self.basket.position  # Simulate basket position
        self.game.check_collision()
        self.assertEqual(self.game.score, initial_score + 1, "Score should increase by 1 when catching an object")

    def test_missed_falling_objects(self):
        # Functionality 2: Missed falling objects
        self.falling_objects.append(FallingObject(100, self.game.screen_height + 1))  # Position it below the screen
        initial_missed = self.game.missed_objects
        self.game.check_collision()
        self.assertEqual(self.game.missed_objects, initial_missed + 1, "Missed objects should increase by 1 when an object hits the ground")

    def test_scoring_system(self):
        # Functionality 3: Catch multiple falling objects
        self.falling_objects.append(FallingObject(self.basket.position + 10, 0))
        self.game.check_collision()  # Catch first object
        self.falling_objects.append(FallingObject(self.basket.position + 10, 0))
        self.game.check_collision()  # Catch second object
        self.assertEqual(self.game.score, 2, "Score should reflect the total number of objects caught")

    def test_game_end_conditions(self):
        # Functionality 4: End game after missing objects
        self.game.missed_objects = 2  # Set to just below the threshold
        self.falling_objects.append(FallingObject(100, self.game.screen_height + 1))  # Miss one more object
        self.game.check_collision()
        self.assertFalse(self.game.running, "Game should end after missing 3 objects")

    def test_save_score_functionality(self):
        # Functionality 5: Save score functionality (not implemented in codebase)
        self.fail("Save score functionality is not implemented in the codebase")

    def test_load_score_functionality(self):
        # Functionality 5: Load score functionality (not implemented in codebase)
        self.fail("Load score functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
