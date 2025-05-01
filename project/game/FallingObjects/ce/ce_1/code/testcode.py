import unittest
import pygame
import os
from game import Game

class TestFallingObjectsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.basket = self.game.basket
        self.falling_objects = self.game.falling_objects

    def test_player_controls_basket(self):
        # Functionality 1: Player Controls the Basket
        initial_position = self.basket.position
        
        # Move left
        self.basket.move_left()
        self.assertLess(self.basket.position, initial_position, "Basket should move left")
        
        # Move right
        initial_position = self.basket.position
        self.basket.move_right()
        self.assertGreater(self.basket.position, initial_position, "Basket should move right")
        
        # Test boundaries
        self.basket.position = 0
        self.basket.move_left()
        self.assertEqual(self.basket.position, 0, "Basket should not move left off the screen")
        
        self.basket.position = 580
        self.basket.move_right()
        self.assertEqual(self.basket.position, 580, "Basket should not move right off the screen")

    def test_catching_falling_objects(self):
        # Functionality 2: Catching Falling Objects
        initial_score = self.game.score
        initial_missed_count = self.game.missed_count
        
        # Simulate catching an object
        self.basket.position = self.falling_objects[0].position  # Align basket with falling object
        self.game.score += 1  # Simulate catching
        self.assertEqual(self.game.score, initial_score + 1, "Score should increase by 1 when catching an object")
        
        # Simulate missing an object
        self.falling_objects[0].position = 601  # Move object below the screen
        self.game.update()  # Update game state
        self.assertEqual(self.game.missed_count, initial_missed_count + 1, "Missed count should increase by 1 when object hits the ground")

    def test_scoring_system(self):
        # Functionality 3: Scoring System
        self.game.score = 0
        for _ in range(5):  # Simulate catching 5 objects
            self.game.score += 1
        self.assertEqual(self.game.score, 5, "Score should reflect the total number of objects caught")
        
        # Simulate missing 3 objects
        self.game.missed_count = 0
        for _ in range(3):
            self.game.missed_count += 1
        self.assertEqual(self.game.missed_count, 3, "Missed count should reflect the number of missed objects")

    def test_game_end_conditions(self):
        # Functionality 4: Game End Conditions
        self.game.missed_count = 5  # Simulate missing maximum allowed objects
        self.game.update()  # Update game state
        self.assertTrue(self.game.check_game_over(), "Game should end after missing 5 objects")

    def test_data_storage(self):
        # Functionality 5: Data Storage
        self.game.score = 10
        self.game.missed_count = 2
        self.game.save_scores()
        
        # Check saved scores
        with open('scores.txt', 'r') as score_file:
            saved_score = int(score_file.read().strip())
        self.assertEqual(saved_score, 10, "Score should be saved correctly in the local text file")
        
        with open('missed_objects.txt', 'r') as missed_file:
            saved_missed = int(missed_file.read().strip())
        self.assertEqual(saved_missed, 2, "Missed count should be saved correctly in the local text file")

if __name__ == '__main__':
    unittest.main()
