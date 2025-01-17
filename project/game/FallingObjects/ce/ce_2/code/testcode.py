import unittest
import pygame
from game import Game
from object import Object

class TestFallingObjectsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()

    def test_player_controls_basket(self):
        # Functionality 1: Player Controls the Basket
        # Test initial position of the basket
        self.assertEqual(self.game.basket_x, 300, "Basket should start at the bottom center of the screen")

        # Test basket moves left
        initial_x = self.game.basket_x
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
        self.game.check_events()
        self.assertLess(self.game.basket_x, initial_x, "Basket should move left")

        # Test basket moves right
        initial_x = self.game.basket_x
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
        self.game.check_events()
        self.assertGreater(self.game.basket_x, initial_x, "Basket should move right")

    def test_catching_falling_objects(self):
        # Functionality 2: Catching Falling Objects
        # Simulate catching an object
        obj = Object(self.game.basket_x, self.game.screen_height - self.game.basket_height - 1, 1)
        self.game.falling_objects.append(obj)
        self.game.update_falling_objects()
        self.assertEqual(self.game.score, 1, "Score should increase by 1 when object is caught")

        # Simulate missing an object
        obj = Object(self.game.basket_x, self.game.screen_height + 1, 1)
        self.game.falling_objects.append(obj)
        self.game.check_miss()
        self.assertEqual(self.game.missed_objects, 1, "Missed objects should increase by 1 when object is missed")

    def test_scoring_system(self):
        # Functionality 3: Scoring System
        # Simulate catching multiple objects
        for _ in range(3):
            obj = Object(self.game.basket_x, self.game.screen_height - self.game.basket_height - 1, 1)
            self.game.falling_objects.append(obj)
        self.game.update_falling_objects()
        self.assertEqual(self.game.score, 3, "Score should reflect the total number of objects caught")

        # Simulate missing objects
        for _ in range(3):
            obj = Object(self.game.basket_x, self.game.screen_height + 1, 1)
            self.game.falling_objects.append(obj)
        self.game.check_miss()
        self.assertEqual(self.game.missed_objects, 3, "Missed objects should reflect the total number of objects missed")

    def test_game_end_conditions(self):
        # Functionality 4: Game End Conditions
        # Simulate game end by missing maximum allowed objects
        self.game.missed_objects = 3
        self.assertFalse(self.game.run(), "Game should end when maximum allowed objects are missed")

    def test_data_storage(self):
        # Functionality 5: Data Storage
        # Simulate saving score
        self.game.score = 5
        self.game.save_data()
        with open('score.txt', 'r') as score_file:
            saved_score = int(score_file.read())
        self.assertEqual(saved_score, 5, "Score should be correctly saved in the local text file")

        # Simulate loading score
        self.game.load_data()
        self.assertEqual(self.game.score, 5, "Previously saved score should be loaded correctly from the local text file")

if __name__ == '__main__':
    unittest.main()
