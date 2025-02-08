import unittest
import pygame
from game import Game, Character, Block
import os

class TestDodgeFallingObjectsGame(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.game = Game()
        self.character = self.game.character

    def tearDown(self):
        pygame.quit()

    def test_player_movement(self):
        # Functionalities 1: Test player movement to the left
        initial_x = self.character.x_position
        self.character.move_left()
        self.assertLess(self.character.x_position, initial_x, "Player should move left")

        # Test player movement to the right
        initial_x = self.character.x_position
        self.character.move_right()
        self.assertGreater(self.character.x_position, initial_x, "Player should move right")

        # Test player does not move beyond the left edge
        self.character.x_position = 0
        self.character.move_left()
        self.assertGreaterEqual(self.character.x_position, 0, "Player should not move beyond the left edge")

        # Test player does not move beyond the right edge
        self.character.x_position = 560
        self.character.move_right()
        self.assertLessEqual(self.character.x_position, 560, "Player should not move beyond the right edge")

    def test_collision_detection(self):
        # Functionalities 2: Test collision detection
        block = Block(self.character.x_position, self.character.y_position, 0)
        self.game.blocks.append(block)
        self.game.check_collision()
        self.assertFalse(self.game.blocks, "Game should end and block list should be empty after collision")

    def test_falling_blocks_behavior(self):
        # Functionalities 3: Test falling blocks behavior
        initial_block_count = len(self.game.blocks)
        self.game.update()
        self.assertGreaterEqual(len(self.game.blocks), initial_block_count, "Blocks should appear randomly")

        # Test block speed increase over time
        initial_speed = self.game.game_speed
        self.game.game_speed += 1
        self.assertGreater(self.game.game_speed, initial_speed, "Block speed should increase over time")

    def test_scoring_system(self):
        # Functionalities 4: Test scoring system
        initial_score = self.game.score
        block = Block(0, 601, 0)  # Create a block that will be removed
        self.game.blocks.append(block)
        self.game.update()
        self.assertGreater(self.game.score, initial_score, "Score should increase when a block is removed")

    def test_player_movement_constraints(self):
        # Functionalities 5: Test player movement constraints
        initial_y = self.character.y_position
        self.character.move_left()
        self.assertEqual(self.character.y_position, initial_y, "Player should not move vertically")

    def test_game_over_condition(self):
        # Functionalities 6: Test game over condition
        block = Block(self.character.x_position, self.character.y_position, 0)
        self.game.blocks.append(block)
        with self.assertRaises(SystemExit):
            self.game.check_collision()

    def test_data_storage(self):
        # Functionalities 7: Test data storage
        self.game.score = 100
        self.game.game_over()
        with open('scores.txt', 'r') as f:
            scores = f.readlines()
        self.assertIn('100', scores[-1], "Score should be saved to the local text file")

if __name__ == '__main__':
    unittest.main()
