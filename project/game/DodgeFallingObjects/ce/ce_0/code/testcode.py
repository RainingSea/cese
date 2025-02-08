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
        self.block = Block(375, 5)

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
        self.player.x_position = 750
        self.player.move('right')
        self.assertEqual(self.player.x_position, 750, "Player should not move beyond the right edge")

    def test_collision_detection(self):
        # Functionality 2: Test collision detection
        self.block.y_position = 550
        self.game.blocks.append(self.block)
        self.game.check_collisions()
        self.assertFalse(self.game.is_running, "Game should end when player collides with a block")

        # Test avoiding collision
        self.game.is_running = True
        self.block.x_position = 0
        self.game.check_collisions()
        self.assertTrue(self.game.is_running, "Game should continue when player avoids a block")

    def test_falling_blocks_behavior(self):
        # Functionality 3: Test falling blocks behavior
        self.block.fall()
        self.assertGreater(self.block.y_position, 0, "Block should fall down")

        # Test increasing speed over time (not implemented in codebase)
        self.fail("Increasing speed of falling blocks over time is not implemented in the codebase")

    def test_scoring_system(self):
        # Functionality 4: Test scoring system
        initial_score = self.game.score
        self.block.y_position = 601
        self.game.blocks.append(self.block)
        self.game.update()
        self.assertGreater(self.game.score, initial_score, "Score should increase when block is removed")

        # Test final score display (not directly testable without UI interaction)

    def test_player_movement_constraints(self):
        # Functionality 5: Test player movement constraints
        initial_y = self.player.x_position
        self.player.move('left')
        self.assertEqual(self.player.x_position, initial_y - 5, "Player should not move vertically")

    def test_game_over_condition(self):
        # Functionality 6: Test game over condition
        self.block.y_position = 550
        self.game.blocks.append(self.block)
        self.game.check_collisions()
        self.assertFalse(self.game.is_running, "Game should end when player collides with a block")

        # Test game reset (not implemented in codebase)
        self.fail("Game reset functionality is not implemented in the codebase")

    def test_data_storage(self):
        # Functionality 7: Test data storage
        self.game.score = 10
        self.game.game_over()
        with open('scores.txt', 'r') as file:
            scores = file.readlines()
        self.assertIn('score: 10\n', scores, "Score should be saved to the local text file")

if __name__ == '__main__':
    unittest.main()
