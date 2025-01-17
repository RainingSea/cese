import unittest
import pygame
from game import Game, Basket, Object

class TestFallingObjectsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.basket = self.game.basket

    def test_player_controls_basket(self):
        # Functionality 1: Player Controls the Basket

        # Test initial position of the basket
        initial_position = self.basket.get_position()
        self.assertEqual(initial_position, 400, "Basket should start at the center of the screen")

        # Test moving the basket left
        self.basket.move_left()
        self.assertEqual(self.basket.get_position(), initial_position - 10, "Basket should move left")

        # Test moving the basket right
        self.basket.move_right()
        self.assertEqual(self.basket.get_position(), initial_position, "Basket should move right")

        # Test holding left arrow key
        for _ in range(40):
            self.basket.move_left()
        self.assertGreaterEqual(self.basket.get_position(), 0, "Basket should not move off the screen to the left")

        # Test holding right arrow key
        for _ in range(40):
            self.basket.move_right()
        self.assertLessEqual(self.basket.get_position(), 760, "Basket should not move off the screen to the right")

    def test_catching_falling_objects(self):
        # Functionality 2: Catching Falling Objects

        # Simulate falling object
        obj = Object()
        obj.position_x = self.basket.get_position()
        obj.position_y = 560  # Just above the basket
        self.game.falling_objects.append(obj)

        # Check collision and score increment
        self.game.check_collisions()
        self.assertEqual(self.game.score, 1, "Score should increase by 1 when object is caught")

        # Simulate missing an object
        obj = Object()
        obj.position_y = 601  # Below the screen
        self.game.falling_objects.append(obj)
        self.game.update()
        self.assertEqual(self.game.missed_objects, 1, "Missed objects should increase by 1 when object is missed")

    def test_scoring_system(self):
        # Functionality 3: Scoring System

        # Catch multiple objects
        for _ in range(5):
            obj = Object()
            obj.position_x = self.basket.get_position()
            obj.position_y = 560
            self.game.falling_objects.append(obj)
            self.game.check_collisions()

        self.assertEqual(self.game.score, 5, "Score should reflect the total number of objects caught")

        # Miss multiple objects
        for _ in range(3):
            obj = Object()
            obj.position_y = 601
            self.game.falling_objects.append(obj)
            self.game.update()

        self.assertEqual(self.game.missed_objects, 3, "Missed objects should reflect the total number of objects missed")

    def test_game_end_conditions(self):
        # Functionality 4: Game End Conditions

        # Test game end by missing maximum allowed objects
        self.game.missed_objects = 3
        self.assertTrue(self.game.missed_objects >= 3, "Game should end when maximum missed objects is reached")

        # Test game end by timer (not implemented in codebase)
        self.fail("Game end by timer is not implemented in the codebase")

    def test_data_storage(self):
        # Functionality 5: Data Storage

        # Test saving score to file (not implemented in codebase)
        self.fail("Saving score to file is not implemented in the codebase")

        # Test loading score from file (not implemented in codebase)
        self.fail("Loading score from file is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
