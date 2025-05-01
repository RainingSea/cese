import unittest
import pygame
import os
from game import Game

class TestFallingObjectsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()

    def test_player_controls_basket(self):
        # Functionality 1: Player Controls the Basket
        initial_position = self.game.basket.position
        
        # Move left
        self.game.basket.move_left()
        self.assertLess(self.game.basket.position, initial_position, "Basket should move left")
        
        # Move right
        initial_position = self.game.basket.position
        self.game.basket.move_right()
        self.assertGreater(self.game.basket.position, initial_position, "Basket should move right")
        
        # Test boundaries
        self.game.basket.position = 0
        self.game.basket.move_left()
        self.assertEqual(self.game.basket.position, 0, "Basket should not move left off the screen")
        
        self.game.basket.position = 580
        self.game.basket.move_right()
        self.assertEqual(self.game.basket.position, 580, "Basket should not move right off the screen")

    def test_catching_falling_objects(self):
        # Functionality 2: Catching Falling Objects
        initial_score = self.game.score
        initial_missed = self.game.missed_objects
        
        # Simulate catching an object
        self.game.basket.position = self.game.falling_objects[0].position
        self.game.falling_objects[0].position = 550  # Position it to be caught
        self.game.check_collision()
        self.assertEqual(self.game.score, initial_score + 1, "Score should increase by 1 when catching an object")
        
        # Simulate missing an object
        self.game.falling_objects[0].position = 601  # Position it to miss
        self.game.update()
        self.assertEqual(self.game.missed_objects, initial_missed + 1, "Missed objects should increase by 1 when an object hits the ground")

    def test_scoring_system(self):
        # Functionality 3: Scoring System
        for _ in range(5):
            self.game.basket.position = self.game.falling_objects[0].position
            self.game.falling_objects[0].position = 550  # Position it to be caught
            self.game.check_collision()
        
        self.assertEqual(self.game.score, 5, "Score should reflect the total number of objects caught")
        
        # Simulate missing objects
        for _ in range(3):
            self.game.falling_objects[0].position = 601  # Position it to miss
            self.game.update()
        
        self.assertEqual(self.game.missed_objects, 3, "Missed objects should reflect the number of objects missed")

    def test_game_end_conditions(self):
        # Functionality 4: Game End Conditions
        self.game.missed_objects = 3
        self.game.end_game()
        self.assertTrue(os.path.exists('game_data.txt'), "Game data file should exist after game ends")
        
        with open('game_data.txt', 'r') as f:
            data = f.read()
            self.assertIn('missed:3', data, "Game data should reflect missed objects")

    def test_data_storage(self):
        # Functionality 5: Data Storage
        self.game.score = 10
        self.game.missed_objects = 2
        self.game.end_game()
        
        with open('game_data.txt', 'r') as f:
            data = f.read()
            self.assertIn('score:10', data, "Score should be saved in the local text file")
            self.assertIn('missed:2', data, "Missed objects should be saved in the local text file")

if __name__ == '__main__':
    unittest.main()
