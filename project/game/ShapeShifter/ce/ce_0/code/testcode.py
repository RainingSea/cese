import unittest
import pygame
import os

# Assuming the main.py is in the same directory as this test file
from main import Game, Shape, Pattern

class TestShapeShifterGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.game.load_shapes()
        self.game.load_target_patterns()

    def test_select_geometric_shapes(self):
        # Functionalities 1: Select a square shape from the available shapes
        square_shape = self.game.shapes[0]  # Assuming the first shape is square
        self.assertEqual(square_shape.type, 'square', "Square shape should be added to the game area")

    def test_rotate_shapes(self):
        # Functionalities 2: Rotate the selected triangle shape 90 degrees clockwise
        triangle_shape = self.game.shapes[1]  # Assuming the second shape is triangle
        initial_rotation = triangle_shape.rotation
        triangle_shape.rotate()
        self.assertEqual(triangle_shape.rotation, (initial_rotation + 90) % 360, "Triangle should be rotated 90 degrees clockwise")

    def test_position_shapes(self):
        # Functionalities 3: Drag the selected circle shape to a different position
        circle_shape = self.game.shapes[2]  # Assuming the third shape is circle
        new_position = (400, 400)
        circle_shape.set_position(new_position)
        self.assertEqual(circle_shape.position, new_position, "Circle shape should move to the new position")

    def test_verify_match_with_target_pattern(self):
        # Functionalities 4: Arrange the shapes to match the target pattern
        self.game.shapes = [Shape('square', (100, 150), 0),
                            Shape('triangle', (200, 250), 90),
                            Shape('circle', (300, 350), 0)]
        self.assertTrue(self.game.check_arrangement(), "Arrangement should match the target pattern")

    def test_provide_feedback_for_incorrect_arrangement(self):
        # Functionalities 5: Arrange shapes in an incorrect pattern
        self.game.shapes = [Shape('circle', (300, 350), 0),
                            Shape('triangle', (200, 250), 90),
                            Shape('square', (100, 150), 0)]
        self.assertFalse(self.game.check_arrangement(), "Arrangement should not match the target pattern")

    def test_reset_the_puzzle(self):
        # Functionalities 6: Reset the puzzle
        original_shapes = self.game.shapes.copy()
        self.game.reset_game()
        self.assertNotEqual(self.game.shapes, original_shapes, "Game should reset the arrangement back to the original state")

if __name__ == '__main__':
    unittest.main()
