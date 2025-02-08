import unittest
from main import CalculationAssistant

class TestCalculationAssistant(unittest.TestCase):

    def setUp(self):
        self.calculator = CalculationAssistant()

    def test_basic_arithmetic_operations(self):
        # Functionalities 1: Perform Basic Arithmetic Operations
        # Test addition
        self.assertEqual(self.calculator.add(5, 3), 8)
        # Test subtraction
        self.assertEqual(self.calculator.subtract(7, -2), 9)
        # Test multiplication
        self.assertEqual(self.calculator.multiply(4, 6), 24)
        # Test division
        self.assertEqual(self.calculator.divide(8, 2), 4)
        # Test division by zero
        with self.assertRaises(ValueError):
            self.calculator.divide(10, 0)

    def test_square_root_calculations(self):
        # Functionalities 2: Calculate Square Roots
        # Test square root of a positive number
        self.assertEqual(self.calculator.square_root(16), 4)
        # Test square root of zero
        self.assertEqual(self.calculator.square_root(0), 0)
        # Test square root of a negative number
        with self.assertRaises(ValueError):
            self.calculator.square_root(-9)

    def test_exponentiation_calculations(self):
        # Functionalities 3: Perform Exponentiation Calculations
        # Test positive base and exponent
        self.assertEqual(self.calculator.exponentiate(2, 3), 8)
        # Test base zero and positive exponent
        self.assertEqual(self.calculator.exponentiate(0, 5), 0)
        # Test positive base and zero exponent
        self.assertEqual(self.calculator.exponentiate(7, 0), 1)
        # Test negative base and even exponent
        self.assertEqual(self.calculator.exponentiate(-3, 2), 9)

    def test_percentage_calculations(self):
        # Functionalities 4: Calculate Percentages
        # Test positive number and percentage
        self.assertEqual(self.calculator.calculate_percentage(200, 10), 20)
        # Test zero and any percentage
        self.assertEqual(self.calculator.calculate_percentage(0, 25), 0)
        # Test negative number and percentage
        self.assertEqual(self.calculator.calculate_percentage(-50, 10), -5)

if __name__ == '__main__':
    unittest.main()
