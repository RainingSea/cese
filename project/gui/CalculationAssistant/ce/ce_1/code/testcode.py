import unittest
from calculations import CalculationAssistant

class TestCalculationAssistant(unittest.TestCase):

    def setUp(self):
        self.calculator = CalculationAssistant()

    def test_basic_arithmetic_operations(self):
        # Functionalities 1: Perform Basic Arithmetic Operations
        # Test addition
        self.assertEqual(self.calculator.perform_addition(5, 3), 8)
        # Test subtraction
        self.assertEqual(self.calculator.perform_subtraction(7, -2), 9)
        # Test multiplication
        self.assertEqual(self.calculator.perform_multiplication(4, 6), 24)
        # Test division
        self.assertEqual(self.calculator.perform_division(8, 2), 4)
        # Test division by zero
        with self.assertRaises(ValueError):
            self.calculator.perform_division(10, 0)

    def test_calculate_square_roots(self):
        # Functionalities 2: Calculate Square Roots
        # Test square root of positive number
        self.assertEqual(self.calculator.calculate_square_root(16), 4)
        # Test square root of zero
        self.assertEqual(self.calculator.calculate_square_root(0), 0)
        # Test square root of negative number
        with self.assertRaises(ValueError):
            self.calculator.calculate_square_root(-9)

    def test_exponentiation_calculations(self):
        # Functionalities 3: Perform Exponentiation Calculations
        # Test positive base and exponent
        self.assertEqual(self.calculator.perform_exponentiation(2, 3), 8)
        # Test base zero and positive exponent
        self.assertEqual(self.calculator.perform_exponentiation(0, 5), 0)
        # Test positive base and zero exponent
        self.assertEqual(self.calculator.perform_exponentiation(7, 0), 1)
        # Test negative base and even exponent
        self.assertEqual(self.calculator.perform_exponentiation(-3, 2), 9)

    def test_calculate_percentages(self):
        # Functionalities 4: Calculate Percentages
        # Test positive number and percentage
        self.assertEqual(self.calculator.calculate_percentage(200, 10), 20)
        # Test zero and any percentage
        self.assertEqual(self.calculator.calculate_percentage(0, 25), 0)
        # Test negative number and percentage
        self.assertEqual(self.calculator.calculate_percentage(-50, 10), -5)

if __name__ == '__main__':
    unittest.main()
