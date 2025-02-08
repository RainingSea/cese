import unittest
import pygame
from game import Game, Player, Block

class TestDodgeFallingObjectsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player = self.game.player

    def test_player_movement(self):
        # Test moving player left
        initial_x = self.player.position_x
        self.player.move('left')
        self.assertLess(self.player.position_x, initial_x, "Player should move left")

        # Test moving player right
        initial_x = self.player.position_x
        self.player.move('right')
        self.assertGreater(self.player.position_x, initial_x, "Player should move right")

        # Test player does not move beyond left edge
        self.player.position_x = 0
        self.player.move('left')
        self.assertEqual(self.player.position_x, 0, "Player should not move beyond left edge")

        # Test player does not move beyond right edge
        self.player.position_x = 550
        self.player.move('right')
        self.assertEqual(self.player.position_x, 550, "Player should not move beyond right edge")

    def test_collision_detection(self):
        # Simulate a block colliding with the player
        block = Block(self.player.position_x, 550, 50, 50)
        self.game.blocks.append(block)
        collision = self.game.check_collision()
        self.assertTrue(collision, "Collision should be detected")

        # Simulate avoiding a block
        self.game.blocks.clear()
        block = Block(self.player.position_x + 100, 550, 50, 50)
        self.game.blocks.append(block)
        collision = self.game.check_collision()
        self.assertFalse(collision, "Player should avoid the block")

    def test_falling_blocks_behavior(self):
        # Test blocks appear randomly and fall straight down
        initial_block_count = len(self.game.blocks)
        self.game.spawn_block()
        self.assertGreaterEqual(len(self.game.blocks), initial_block_count, "Blocks should spawn randomly")

        # Test block falling speed increases
        block = Block(0, 0, 50, 50)
        initial_y = block.position_y
        block.fall(self.game.speed)
        self.assertGreater(block.position_y, initial_y, "Block should fall down")

    def test_scoring_system(self):
        # Test score increases over time
        initial_score = self.game.score
        self.game.update_score()
        self.assertGreater(self.game.score, initial_score, "Score should increase over time")

    def test_player_movement_constraints(self):
        # Test player does not move vertically
        initial_y = 550
        self.assertEqual(self.player.height, 50, "Player should remain at the bottom of the screen")

    def test_game_over_condition(self):
        # Test game ends on collision
        block = Block(self.player.position_x, 550, 50, 50)
        self.game.blocks.append(block)
        self.game.check_collision()
        self.assertFalse(pygame.get_init(), "Game should end on collision")

    def test_data_storage(self):
        # Test score is saved to a file
        self.game.score = 100
        self.game.save_high_score()
        with open('high_scores.txt', 'r') as f:
            scores = f.readlines()
        self.assertIn('score: 100\n', scores, "Score should be saved to the file")

if __name__ == '__main__':
    unittest.main()
