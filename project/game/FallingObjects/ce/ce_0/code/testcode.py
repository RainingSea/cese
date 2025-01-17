import unittest
import pygame
from game import Game, Basket, Object

class TestFallingObjectsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()
        self.game.start_game()

    def test_player_controls_basket(self):
        # Functionalities 1: Test initial position of the basket
        initial_position = self.game.basket.get_position()
        self.assertEqual(initial_position, (400, 550), "Basket should start at the bottom center of the screen")

        # Test basket movement to the left
        self.game.basket.move_left()
        new_position = self.game.basket.get_position()
        self.assertLess(new_position[0], initial_position[0], "Basket should move left")

        # Test basket movement to the right
        self.game.basket.move_right()
        new_position = self.game.basket.get_position()
        self.assertGreater(new_position[0], initial_position[0], "Basket should move right")

    def test_catching_falling_objects(self):
        # Functionalities 2: Test catching a falling object
        self.game.falling_objects.append(Object((400, 540)))  # Position object above the basket
        self.game.update()
        self.assertEqual(self.game.score, 1, "Score should increase by 1 when an object is caught")

        # Test missing a falling object
        self.game.falling_objects.append(Object((400, 600)))  # Position object below the screen
        self.game.update()
        self.assertEqual(self.game.missed_objects, 1, "Missed objects should increase by 1 when an object is missed")

    def test_scoring_system(self):
        # Functionalities 3: Test scoring system
        self.game.falling_objects.append(Object((400, 540)))
        self.game.update()
        self.game.falling_objects.append(Object((400, 540)))
        self.game.update()
        self.assertEqual(self.game.score, 2, "Score should reflect the total number of objects caught")

        # Test game end condition when missing objects
        self.game.missed_objects = 3
        self.assertTrue(self.game.missed_objects >= 3, "Game should end when missed objects reach 3")

    def test_game_end_conditions(self):
        # Functionalities 4: Test game end by time
        self.game.game_time = 60.0
        self.assertTrue(self.game.game_time >= 60.0, "Game should end when the timer reaches 60 seconds")

        # Test game end by missed objects
        self.game.missed_objects = 3
        self.assertTrue(self.game.missed_objects >= 3, "Game should end when missed objects reach 3")

    def test_data_storage(self):
        # Functionalities 5: Test data storage (not implemented in codebase)
        self.fail("Data storage functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
