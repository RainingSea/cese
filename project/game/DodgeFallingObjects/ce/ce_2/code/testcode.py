import unittest
import pygame
import random
from game import Game, Player, Block

class TestDodgeFallingObjectsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player = self.game.player
        self.blocks = self.game.blocks

    def test_player_movement(self):
        # Functionalities 1 Test player movement to the left
        initial_x = self.player.position_x
        self.player.move_left()
        self.assertLess(self.player.position_x, initial_x, "Player should move left")

        # Test player movement to the right
        initial_x = self.player.position_x
        self.player.move_right()
        self.assertGreater(self.player.position_x, initial_x, "Player should move right")

        # Test player movement beyond the left edge
        self.player.position_x = 0
        self.player.move_left()
        self.assertEqual(self.player.position_x, 0, "Player should not move beyond the left edge")

        # Test player movement beyond the right edge
        self.player.position_x = 590  # Assuming player width is 50
        self.player.move_right()
        self.assertEqual(self.player.position_x, 590, "Player should not move beyond the right edge")

    def test_collision_detection(self):
        # Functionalities 2 Simulate a collision
        self.player.position_x = 300  # Center player
        block = Block()
        block.position_x = 300
        block.position_y = 450  # Position block to collide with player
        self.blocks.append(block)

        self.game.check_collision()
        self.assertFalse(self.game.running, "Game should end on collision")

        # Test avoiding a block
        self.game.running = True  # Reset game state
        self.blocks.clear()  # Clear blocks
        block.position_y = 400  # Position block above player
        self.blocks.append(block)
        self.player.move_left()  # Move player to avoid
        self.game.check_collision()
        self.assertTrue(self.game.running, "Game should continue if player avoids block")

    def test_falling_blocks_behavior(self):
        # Functionalities 3 Test falling blocks
        initial_block_count = len(self.blocks)
        self.game.update()  # Update game to potentially add blocks
        self.assertGreaterEqual(len(self.blocks), initial_block_count, "Blocks should appear randomly")

        # Test speed of falling blocks
        block = Block()
        initial_speed = block.speed
        block.fall()
        self.assertGreater(block.position_y, 0, "Block should fall downwards")

    def test_scoring_system(self):
        # Functionalities 4 Test scoring system
        initial_score = self.game.score
        self.blocks.append(Block())  # Add a block to fall
        self.game.update()  # Update game to potentially increase score
        self.assertGreaterEqual(self.game.score, initial_score, "Score should increase over time survived")

        # Test score on collision
        self.game.running = True  # Reset game state
        self.blocks.clear()  # Clear blocks
        block = Block()
        block.position_y = 450  # Position block to collide with player
        self.blocks.append(block)
        self.game.check_collision()
        self.assertEqual(self.game.score, initial_score + 1, "Final score should reflect time survived")

    def test_player_movement_constraints(self):
        # Functionalities 5 Test vertical movement constraint
        initial_y = self.player.position_x  # Player should not change vertical position
        self.player.move_left()  # Only horizontal movement
        self.assertEqual(self.player.position_x, initial_y, "Player should not move vertically")

    def test_game_over_condition(self):
        # Functionalities 6 Test game over condition
        self.player.position_x = 300
        block = Block()
        block.position_x = 300
        block.position_y = 450
        self.blocks.append(block)

        self.game.check_collision()
        self.assertFalse(self.game.running, "Game should end on collision")

    def test_data_storage(self):
        # Functionalities 7 Test score saving (not implemented in codebase)
        self.fail("Data storage functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
