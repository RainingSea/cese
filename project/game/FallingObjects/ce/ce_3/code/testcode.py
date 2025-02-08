import unittest
import pygame
from game import Game, Basket, FallingObject

class TestFallingObjectsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.basket = self.game.basket

    def test_basket_movement(self):
        # Test basket movement to the left
        initial_x = self.basket.position[0]
        self.basket.move_left()
        self.assertLess(self.basket.position[0], initial_x, "Basket should move left")

        # Test basket movement to the right
        initial_x = self.basket.position[0]
        self.basket.move_right()
        self.assertGreater(self.basket.position[0], initial_x, "Basket should move right")

    def test_falling_object_creation(self):
        # Test if a falling object is created
        initial_count = len(self.game.falling_objects)
        self.game.spawn_falling_object()
        self.assertEqual(len(self.game.falling_objects), initial_count + 1, "A new falling object should be created")

    def test_falling_object_fall(self):
        # Test if falling objects fall
        falling_object = FallingObject([100, 0], 5)
        initial_y = falling_object.position[1]
        falling_object.fall()
        self.assertEqual(falling_object.position[1], initial_y + 5, "Falling object should fall down by its speed")

    def test_collision_detection(self):
        # Test collision detection between basket and falling object
        falling_object = FallingObject([self.basket.position[0] + 50, self.basket.position[1]], 0)
        self.game.falling_objects.append(falling_object)
        initial_score = self.game.score
        self.game.check_collision()
        self.assertEqual(self.game.score, initial_score + 1, "Score should increase when basket catches a falling object")

    def test_missed_object_count(self):
        # Test if missed objects are counted
        falling_object = FallingObject([100, 601], 5)  # Position beyond the screen height
        self.game.falling_objects.append(falling_object)
        initial_missed = self.game.missed_objects
        self.game.update()
        self.assertEqual(self.game.missed_objects, initial_missed + 1, "Missed objects count should increase when an object falls beyond the screen")

    def test_game_end_data_saving(self):
        # Test if game data is saved correctly at the end
        self.game.score = 5
        self.game.missed_objects = 3
        self.game.end_game()
        with open('game_data.txt', 'r') as file:
            data = file.readlines()
            self.assertEqual(int(data[0].strip()), 5, "Score should be saved correctly")
            self.assertEqual(int(data[1].strip()), 3, "Missed objects count should be saved correctly")

if __name__ == '__main__':
    unittest.main()
