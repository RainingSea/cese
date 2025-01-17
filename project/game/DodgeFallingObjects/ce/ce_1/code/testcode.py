import unittest
import pygame
from game import Game
from player import Player
from block import Block

class TestDodgeFallingObjectsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player = self.game.player

    def test_player_movement(self):
        # Functionality 1: Test player movement to the left
        initial_x = self.player.x_position
        self.player.move('left')
        self.assertLess(self.player.x_position, initial_x, "Player should move left")

        # Test player movement to the right
        initial_x = self.player.x_position
        self.player.move('right')
        self.assertGreater(self.player.x_position, initial_x, "Player should move right")

        # Test player does not move beyond the left edge
        self.player.x_position = 0
        self.player.move('left')
        self.assertEqual(self.player.x_position, 0, "Player should not move beyond the left edge")

        # Test player does not move beyond the right edge
        self.player.x_position = 800 - self.player.width
        self.player.move('right')
        self.assertEqual(self.player.x_position, 800 - self.player.width, "Player should not move beyond the right edge")

    def test_collision_detection(self):
        # Functionality 2: Test collision detection
        block = Block(50)
        block.x_position = self.player.x_position
        block.y_position = self.player.height
        self.assertTrue(self.game.check_collision(block), "Collision should be detected")

        # Test avoiding collision
        block.x_position = self.player.x_position + self.player.width + 1
        self.assertFalse(self.game.check_collision(block), "Collision should not be detected")

    def test_falling_blocks_behavior(self):
        # Functionality 3: Test falling blocks behavior
        initial_y = 0
        block = Block(50)
        block.y_position = initial_y
        block.fall(self.game.block_speed)
        self.assertGreater(block.y_position, initial_y, "Block should fall down")

    def test_scoring_system(self):
        # Functionality 4: Test scoring system
        initial_score = self.game.score
        block = Block(50)
        block.x_position = self.player.x_position
        block.y_position = self.player.height
        self.game.blocks.append(block)
        self.game.update()
        self.assertGreater(self.game.score, initial_score, "Score should increase upon collision")

    def test_player_movement_constraints(self):
        # Functionality 5: Test player movement constraints
        initial_y = self.player.height
        self.player.move('up')
        self.assertEqual(self.player.height, initial_y, "Player should not move vertically")

    def test_game_over_condition(self):
        # Functionality 6: Test game over condition
        block = Block(50)
        block.x_position = self.player.x_position
        block.y_position = self.player.height
        self.game.blocks.append(block)
        self.game.update()
        self.assertFalse(self.game.run(), "Game should end upon collision")

    def test_data_storage(self):
        # Functionality 7: Test data storage
        self.game.save_score()
        with open('scores.txt', 'r') as f:
            scores = f.readlines()
        self.assertIn(f'score: {self.game.score}\n', scores, "Score should be saved to file")

if __name__ == '__main__':
    unittest.main()
