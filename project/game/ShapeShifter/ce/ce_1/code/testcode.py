import unittest
from game import Game
from shapes import Shape
from target_pattern import TargetPattern

class TestShapeShifterGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.game.load_shapes()  # Load shapes from shapes.txt

    def test_select_shape(self):
        # Functionalities 1: Select a square shape from the available shapes
        self.game.select_shape(1)  # Assuming 1 corresponds to square
        self.assertEqual(self.game.selected_shape.type, 'square', "Selected shape should be square")

    def test_rotate_shape(self):
        # Functionalities 2: Rotate the selected triangle shape 90 degrees clockwise
        self.game.select_shape(2)  # Assuming 2 corresponds to triangle
        initial_rotation = self.game.selected_shape.rotation
        self.game.rotate_shape()
        self.assertEqual(self.game.selected_shape.rotation, (initial_rotation + 90) % 360, "Triangle should be rotated 90 degrees")

    def test_position_shape(self):
        # Functionalities 3: Drag the selected circle shape to a different position
        self.game.select_shape(0)  # Assuming 0 corresponds to circle
        self.game.position_shape(100, 150)
        self.assertEqual((self.game.selected_shape.position_x, self.game.selected_shape.position_y), (100, 150), "Circle should be positioned at (100, 150)")

    def test_verify_match_with_target_pattern(self):
        # Functionalities 4: Verify arrangement with target pattern
        self.game.select_shape(0)  # Select circle
        self.game.position_shape(0, 0)  # Position it correctly
        self.game.select_shape(1)  # Select square
        self.game.position_shape(50, 50)  # Position it correctly
        self.assertTrue(self.game.verify_arrangement(), "Arrangement should match the target pattern")

    def test_feedback_incorrect_arrangement(self):
        # Functionalities 5: Provide feedback for incorrect arrangement
        self.game.select_shape(0)  # Select circle
        self.game.position_shape(100, 100)  # Incorrect position
        self.assertFalse(self.game.verify_arrangement(), "Arrangement should not match the target pattern")

    def test_reset_puzzle(self):
        # Functionalities 6: Reset the puzzle
        self.game.select_shape(0)  # Select circle
        self.game.position_shape(100, 100)  # Move it
        self.game.reset_puzzle()
        self.assertEqual((self.game.selected_shape.position_x, self.game.selected_shape.position_y), (0, 0), "Shape should be reset to initial position (0, 0)")

if __name__ == '__main__':
    unittest.main()
