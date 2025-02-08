import unittest
from game import Game, Shape

class TestShapeShifterGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and load shapes and patterns
        self.game = Game()
        self.game.load_shapes()
        self.game.load_patterns()

    def test_select_geometric_shapes(self):
        # Functionalities 1: Select a square shape
        square_shape = next((shape for shape in self.game.shapes if shape.type == "square"), None)
        self.assertIsNotNone(square_shape, "Square shape should be available")
        self.assertEqual(square_shape.position, (200, 150), "Square shape should be at position (200, 150)")

    def test_rotate_shapes(self):
        # Functionalities 2: Rotate the triangle shape
        triangle_shape = next((shape for shape in self.game.shapes if shape.type == "triangle"), None)
        self.assertIsNotNone(triangle_shape, "Triangle shape should be available")
        initial_rotation = triangle_shape.rotation
        triangle_shape.rotate()
        self.assertEqual(triangle_shape.rotation, (initial_rotation + 90) % 360, "Triangle shape should be rotated 90 degrees clockwise")

    def test_position_shapes(self):
        # Functionalities 3: Move the circle shape
        circle_shape = next((shape for shape in self.game.shapes if shape.type == "circle"), None)
        self.assertIsNotNone(circle_shape, "Circle shape should be available")
        new_position = (150, 200)
        circle_shape.move(new_position)
        self.assertEqual(circle_shape.position, new_position, "Circle shape should be moved to the new position")

    def test_verify_match_with_target_pattern(self):
        # Functionalities 4: Verify correct arrangement
        self.assertTrue(self.game.check_arrangement(), "Arrangement should match the target pattern")

    def test_provide_feedback_for_incorrect_arrangement(self):
        # Functionalities 5: Verify incorrect arrangement
        # Move a shape to make the arrangement incorrect
        self.game.shapes[0].move((0, 0))
        self.assertFalse(self.game.check_arrangement(), "Arrangement should not match the target pattern")

    def test_reset_the_puzzle(self):
        # Functionalities 6: Reset the puzzle
        self.game.reset()
        self.assertEqual(len(self.game.shapes), 0, "Shapes should be cleared after reset")
        self.assertFalse(self.game.is_correct, "is_correct should be False after reset")

if __name__ == '__main__':
    unittest.main()
