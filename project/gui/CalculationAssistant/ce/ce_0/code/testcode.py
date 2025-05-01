import unittest
import os
import subprocess
from main import CalculationAssistant

class TestCalculationAssistant(unittest.TestCase):

    def setUp(self):
        self.app = CalculationAssistant()
        self.app.root = None  # Prevent the GUI from opening during tests

    def test_basic_arithmetic_operations(self):
        # Functionalities 1: Perform Basic Arithmetic Operations
        self.assertEqual(self.app.add(5, 3), 8)
        self.assertEqual(self.app.subtract(7, -2), 9)
        self.assertEqual(self.app.multiply(4, 6), 24)
        self.assertEqual(self.app.divide(8, 2), 4)

        # Testing division by zero
        with self.assertRaises(ZeroDivisionError):
            self.app.divide(10, 0)

    def test_square_root(self):
        # Functionalities 2: Calculate Square Roots
        self.assertEqual(self.app.square_root(16), 4)
        self.assertEqual(self.app.square_root(0), 0)

        # Testing invalid input for square root
        with self.assertRaises(ValueError):
            self.app.square_root(-9)

    def test_exponentiation(self):
        # Functionalities 3: Perform Exponentiation Calculations
        self.assertEqual(self.app.exponentiate(2, 3), 8)
        self.assertEqual(self.app.exponentiate(0, 5), 0)
        self.assertEqual(self.app.exponentiate(7, 0), 1)
        self.assertEqual(self.app.exponentiate(-3, 2), 9)

    def test_percentage(self):
        # Functionalities 4: Calculate Percentages
        self.assertEqual(self.app.calculate_percentage(200, 10), 20)
        self.assertEqual(self.app.calculate_percentage(0, 25), 0)
        self.assertEqual(self.app.calculate_percentage(-50, 10), -5)

if __name__ == '__main__':
    unittest.main()
