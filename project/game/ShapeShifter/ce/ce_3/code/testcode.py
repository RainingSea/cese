import unittest
from game import Game, Shape

class TestShapeShifterGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game with shapes and target pattern
        self.shapes = [
            Shape("circle", (0, 0), 0),
            Shape("square", (1, 1), 0),
            Shape("triangle", (2, 2), 0),
            Shape("rectangle", (3, 3), 0)
        ]
        self.target_pattern = [("circle", (0, 0), 0), ("square", (1, 1), 0), ("triangle", (2, 2), 0), ("rectangle", (3, 3), 0)]
        self.game = Game(self.shapes, self.target_pattern)

    def test_select_geometric_shapes(self):
        # Functionalities 1: Select a square shape
        selected_shape = self.game.select_shape(self.shapes[1])  # Selecting square
        self.assertIsNotNone(selected_shape, "Square shape should be selectable")
        self.assertEqual(selected_shape.type, "square", "Selected shape should be a square")

    def test_rotate_shapes(self):
        # Functionalities 2: Rotate the triangle shape 90 degrees
        triangle = self.shapes[2]
        initial_rotation = triangle.rotation
        self.game.rotate_shape(triangle, 90)
        self.assertEqual(triangle.rotation, (initial_rotation + 90) % 360, "Triangle shape should be rotated 90 degrees")

    def test_position_shapes(self):
        # Functionalities 3: Move the circle shape to a new position
        circle = self.shapes[0]
        new_position = (5, 5)
        self.game.position_shape(circle, new_position)
        self.assertEqual(circle.position, new_position, "Circle shape should be moved to the new position")

    def test_verify_match_with_target_pattern(self):
        # Functionalities 4: Verify arrangement matches target pattern
        self.assertTrue(self.game.verify_arrangement(), "Arrangement should match the target pattern")

    def test_provide_feedback_for_incorrect_arrangement(self):
        # Functionalities 5: Verify incorrect arrangement feedback
        self.shapes[0].set_position((10, 10))  # Move circle to incorrect position
        self.assertFalse(self.game.verify_arrangement(), "Arrangement should not match the target pattern")

    def test_reset_the_puzzle(self):
        # Functionalities 6: Reset the puzzle
        self.shapes[0].set_position((10, 10))  # Move circle to incorrect position
        self.game.reset_puzzle()
        for shape, target in zip(self.shapes, self.target_pattern):
            self.assertEqual(shape.position, target[1], "Shape should be reset to initial position")
            self.assertEqual(shape.rotation, target[2], "Shape should be reset to initial rotation")

if __name__ == '__main__':
    unittest.main()
