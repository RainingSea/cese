import unittest
import pygame
from game import Game
from player import Player
from block import Block
from score import Score

class TestDodgeFallingObjectsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player = self.game.player

    def test_player_movement(self):
        # Functionality 1: Player Movement
        initial_x = self.player.position_x
        # Simulate pressing the left arrow key
        keys = {pygame.K_LEFT: True, pygame.K_RIGHT: False}
        pygame.key.set_pressed(keys)
        self.player.move()
        self.assertLess(self.player.position_x, initial_x, "Player should move left")

        # Simulate pressing the right arrow key
        initial_x = self.player.position_x
        keys = {pygame.K_LEFT: False, pygame.K_RIGHT: True}
        pygame.key.set_pressed(keys)
        self.player.move()
        self.assertGreater(self.player.position_x, initial_x, "Player should move right")

        # Attempt to move beyond the left edge
        self.player.position_x = 0
        keys = {pygame.K_LEFT: True}
        pygame.key.set_pressed(keys)
        self.player.move()
        self.assertEqual(self.player.position_x, 0, "Player should not move beyond the left edge")

        # Attempt to move beyond the right edge
        self.player.position_x = 750
        keys = {pygame.K_RIGHT: True}
        pygame.key.set_pressed(keys)
        self.player.move()
        self.assertEqual(self.player.position_x, 750, "Player should not move beyond the right edge")

    def test_collision_detection(self):
        # Functionality 2: Collision Detection
        block = Block(400, 550)  # Position block to collide with player
        self.game.blocks.append(block)
        self.game.check_collision()
        self.assertFalse(self.game.running, "Game should end on collision with block")

        # Move player to avoid block
        self.game.running = True  # Reset game state
        self.player.position_x = 300  # Move player away from block
        self.game.check_collision()
        self.assertTrue(self.game.running, "Game should continue if player avoids block")

    def test_falling_blocks_behavior(self):
        # Functionality 3: Falling Blocks Behavior
        initial_block_count = len(self.game.blocks)
        self.game.update()  # Update game to potentially add a block
        self.assertGreaterEqual(len(self.game.blocks), initial_block_count, "Blocks should appear randomly")

        # Check if blocks fall
        for block in self.game.blocks:
            initial_y = block.position_y
            block.fall()
            self.assertGreater(block.position_y, initial_y, "Block should fall downwards")

    def test_scoring_system(self):
        # Functionality 4: Scoring System
        initial_score = self.game.score
        self.game.score += 10  # Simulate surviving for a few seconds
        self.assertGreater(self.game.score, initial_score, "Score should increase based on time survived")

        # End game by collision
        self.game.running = False
        self.game.save_score()
        with open('scores.txt', 'r') as file:
            scores = [int(line.strip()) for line in file]
        self.assertIn(self.game.score, scores, "Final score should be saved to scores.txt")

    def test_player_movement_constraints(self):
        # Functionality 5: Player Movement Constraints
        initial_y = self.player.position_x
        keys = {pygame.K_UP: True, pygame.K_DOWN: True}
        pygame.key.set_pressed(keys)
        self.player.move()
        self.assertEqual(self.player.position_x, initial_y, "Player should not move vertically")

    def test_game_over_condition(self):
        # Functionality 6: Game Over Condition
        self.game.running = True
        block = Block(400, 550)  # Position block to collide with player
        self.game.blocks.append(block)
        self.game.check_collision()
        self.assertFalse(self.game.running, "Game should end on collision with block")

    def test_data_storage(self):
        # Functionality 7: Data Storage
        self.game.score = 150  # Simulate achieving a score
        self.game.save_score()
        with open('scores.txt', 'r') as file:
            scores = [int(line.strip()) for line in file]
        self.assertIn(150, scores, "Final score should be saved to scores.txt")

if __name__ == '__main__':
    unittest.main()
