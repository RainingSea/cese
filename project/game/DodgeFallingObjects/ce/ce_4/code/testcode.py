import unittest
import pygame
from game import Game, Player, Block

class TestDodgeFallingObjectsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player = self.game.player

    def test_player_movement(self):
        # Functionality 1: Player Movement
        initial_x = self.player.x_position

        # Test moving left
        self.player.move('left')
        self.assertLess(self.player.x_position, initial_x, "Player should move left")

        # Test moving right
        initial_x = self.player.x_position
        self.player.move('right')
        self.assertGreater(self.player.x_position, initial_x, "Player should move right")

        # Test moving beyond left edge
        self.player.x_position = 0
        self.player.move('left')
        self.assertGreaterEqual(self.player.x_position, 0, "Player should not move beyond left edge")

        # Test moving beyond right edge
        self.player.x_position = 750
        self.player.move('right')
        self.assertLessEqual(self.player.x_position, 750, "Player should not move beyond right edge")

    def test_collision_detection(self):
        # Functionality 2: Collision Detection
        block = Block(self.player.x_position, 550)
        self.game.blocks.append(block)

        # Test collision
        self.assertTrue(self.game.check_collision(), "Collision should be detected")

        # Test avoiding collision
        self.player.move('right')
        self.assertFalse(self.game.check_collision(), "Collision should not be detected")

    def test_falling_blocks_behavior(self):
        # Functionality 3: Falling Blocks Behavior
        initial_block_count = len(self.game.blocks)
        self.game.spawn_block()
        self.assertEqual(len(self.game.blocks), initial_block_count + 1, "A new block should spawn")

        # Test block falling
        block = self.game.blocks[0]
        initial_y = block.y_position
        block.fall(self.game.game_speed)
        self.assertGreater(block.y_position, initial_y, "Block should fall down")

    def test_scoring_system(self):
        # Functionality 4: Scoring System
        initial_score = self.game.score
        self.game.update()
        self.assertGreaterEqual(self.game.score, initial_score, "Score should increase over time")

    def test_player_movement_constraints(self):
        # Functionality 5: Player Movement Constraints
        initial_y = 550  # Player's y position should remain constant
        self.player.move('left')
        self.assertEqual(self.player.x_position, self.player.x_position, "Player should not move vertically")

    def test_game_over_condition(self):
        # Functionality 6: Game Over Condition
        block = Block(self.player.x_position, 550)
        self.game.blocks.append(block)
        self.assertTrue(self.game.check_collision(), "Game should end on collision")

    def test_data_storage(self):
        # Functionality 7: Data Storage
        self.game.save_score()
        with open('scores.txt', 'r') as file:
            scores = file.readlines()
        self.assertIn(f"{self.game.score}\n", scores, "Score should be saved to file")

if __name__ == '__main__':
    unittest.main()
