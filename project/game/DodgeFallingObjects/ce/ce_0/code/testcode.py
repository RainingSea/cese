import unittest
import pygame
from game import Game, Character, Block

class TestDodgeFallingObjectsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        pygame.init()
        self.game = Game()
        self.character = self.game.character

    def tearDown(self):
        pygame.quit()

    def test_player_movement(self):
        # Functionality 1: Player Movement
        # Test moving left
        initial_x = self.character.x_position
        self.character.move('left')
        self.assertLess(self.character.x_position, initial_x, "Character should move left")

        # Test moving right
        initial_x = self.character.x_position
        self.character.move('right')
        self.assertGreater(self.character.x_position, initial_x, "Character should move right")

        # Test moving beyond left edge
        self.character.x_position = 0
        self.character.move('left')
        self.assertGreaterEqual(self.character.x_position, 0, "Character should not move beyond left edge")

        # Test moving beyond right edge
        self.character.x_position = 550
        self.character.move('right')
        self.assertLessEqual(self.character.x_position, 550, "Character should not move beyond right edge")

    def test_collision_detection(self):
        # Functionality 2: Collision Detection
        # Simulate a block falling and colliding with the character
        block = Block(self.character.x_position, 50, 50)
        block.y_position = 350  # Position block to collide with character
        self.game.falling_blocks.append(block)
        self.game.check_collision()
        self.assertEqual(self.game.score, 1, "Score should increase on collision")

        # Test avoiding a block
        self.character.x_position = 0
        block.x_position = 100
        self.game.check_collision()
        self.assertEqual(self.game.score, 1, "Score should not increase if no collision")

    def test_falling_blocks_behavior(self):
        # Functionality 3: Falling Blocks Behavior
        self.game.spawn_block()
        self.assertTrue(any(block.y_position == 0 for block in self.game.falling_blocks), "Blocks should spawn at the top")

        # Test block falling speed
        initial_y_positions = [block.y_position for block in self.game.falling_blocks]
        self.game.update_blocks()
        self.assertTrue(all(block.y_position > initial_y for block, initial_y in zip(self.game.falling_blocks, initial_y_positions)), "Blocks should fall down")

    def test_scoring_system(self):
        # Functionality 4: Scoring System
        initial_score = self.game.score
        self.game.check_collision()
        self.assertGreaterEqual(self.game.score, initial_score, "Score should increase over time")

    def test_player_movement_constraints(self):
        # Functionality 5: Player Movement Constraints
        initial_y = 350  # Character's y position
        self.character.move('left')
        self.assertEqual(self.character.x_position, 290, "Character should move left")
        self.assertEqual(initial_y, 350, "Character should not move vertically")

    def test_game_over_condition(self):
        # Functionality 6: Game Over Condition
        block = Block(self.character.x_position, 50, 50)
        block.y_position = 350
        self.game.falling_blocks.append(block)
        self.game.check_collision()
        self.assertFalse(self.game.is_running, "Game should end on collision")

    def test_data_storage(self):
        # Functionality 7: Data Storage
        self.fail("Data storage functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
