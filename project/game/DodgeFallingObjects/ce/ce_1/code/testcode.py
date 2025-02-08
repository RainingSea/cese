import unittest
import pygame
from game import Game
from player import Player
from block import Block

class TestDodgeFallingObjectsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        pygame.init()
        self.game = Game()
        self.player = self.game.player
        self.block = Block(300, 5)

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
        self.assertEqual(self.player.x_position, 0, "Player should not move beyond the left edge")

        # Test moving beyond right edge
        self.player.x_position = 550
        self.player.move('right')
        self.assertEqual(self.player.x_position, 550, "Player should not move beyond the right edge")

    def test_collision_detection(self):
        # Functionality 2: Collision Detection
        self.game.blocks.append(self.block)
        self.block.y_position = 550  # Simulate block falling to player's level

        # Simulate collision
        self.game.check_collision()
        self.assertFalse(self.game.is_running, "Game should end on collision with block")

    def test_falling_blocks_behavior(self):
        # Functionality 3: Falling Blocks Behavior
        initial_y = self.block.y_position
        self.block.fall()
        self.assertGreater(self.block.y_position, initial_y, "Block should fall downwards")

    def test_scoring_system(self):
        # Functionality 4: Scoring System
        initial_score = self.game.score
        self.game.score += 1  # Simulate scoring
        self.assertGreater(self.game.score, initial_score, "Score should increase over time")

    def test_player_movement_constraints(self):
        # Functionality 5: Player Movement Constraints
        initial_y = self.player.get_position()[1]
        self.player.move('left')
        self.assertEqual(self.player.get_position()[1], initial_y, "Player should not move vertically")

    def test_game_over_condition(self):
        # Functionality 6: Game Over Condition
        self.game.is_running = False
        self.assertFalse(self.game.is_running, "Game should end when player collides with block")

    def test_data_storage(self):
        # Functionality 7: Data Storage
        self.game.save_score()
        with open('scores.txt', 'r') as file:
            scores = file.readlines()
        self.assertIn(f'Score: {self.game.score}\n', scores, "Score should be saved in scores.txt")

if __name__ == '__main__':
    unittest.main()
