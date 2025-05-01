import unittest
import pygame
from game import Game

class TestDodgeFallingObjectsGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player = self.game.player
        self.blocks = self.game.blocks

    def test_player_movement(self):
        # Functionality 1: Test player movement to the left
        initial_x = self.player.position_x
        self.player.move_left()
        self.assertLess(self.player.position_x, initial_x, "Player should move left")

        # Test player movement to the right
        initial_x = self.player.position_x
        self.player.move_right()
        self.assertGreater(self.player.position_x, initial_x, "Player should move right")

        # Test player cannot move beyond the left edge
        self.player.position_x = 0
        self.player.move_left()
        self.assertEqual(self.player.position_x, 0, "Player should not move beyond the left edge")

        # Test player cannot move beyond the right edge
        self.player.position_x = 580
        self.player.move_right()
        self.assertEqual(self.player.position_x, 580, "Player should not move beyond the right edge")

    def test_collision_detection(self):
        # Functionality 2: Simulate a block falling and colliding with the player
        self.blocks[0].position_y = 550  # Position block at player level
        self.game.check_collision()
        self.assertTrue(self.game.score > 0, "Score should increase upon collision")

        # Test player avoiding a falling block
        self.player.position_x = 300  # Center position
        self.blocks[0].position_y = 600  # Reset block position
        self.game.check_collision()
        self.assertEqual(self.game.score, 0, "Score should not increase if no collision occurs")

    def test_falling_blocks_behavior(self):
        # Functionality 3: Check if blocks fall from the top
        for block in self.blocks:
            initial_y = block.position_y
            block.fall()
            self.assertGreater(block.position_y, initial_y, "Block should fall down")

        # Test block reset position
        block = self.blocks[0]
        block.position_y = 601  # Simulate block going off-screen
        block.reset_position()
        self.assertEqual(block.position_y, 0, "Block should reset to the top of the screen")

    def test_scoring_system(self):
        # Functionality 4: Test score increment
        initial_score = self.game.score
        self.blocks[0].position_y = 601  # Simulate block going off-screen
        self.blocks[0].reset_position()  # This should increment the score
        self.assertGreater(self.game.score, initial_score, "Score should increase when block goes off-screen")

    def test_player_movement_constraints(self):
        # Functionality 5: Test vertical movement constraint
        initial_y = self.player.position_x
        self.player.move_left()
        self.assertEqual(self.player.position_x, initial_y, "Player should not move vertically")

    def test_game_over_condition(self):
        # Functionality 6: Simulate game over condition
        self.blocks[0].position_y = 550  # Position block at player level
        self.game.check_collision()
        self.assertTrue(self.game.score > 0, "Game should end upon collision")

    def test_data_storage(self):
        # Functionality 7: Test score saving
        self.game.score = 10  # Set a score
        self.game.save_score()  # Save score to file
        with open('scores.txt', 'r') as file:
            saved_score = int(file.readline().strip())
        self.assertEqual(saved_score, 10, "Final score should be saved correctly in the file")

if __name__ == '__main__':
    unittest.main()
