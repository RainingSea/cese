import unittest
from CalculationAssistant import CalculationAssistant

class TestCalculationAssistant(unittest.TestCase):

    def setUp(self):
        self.calculator = CalculationAssistant()

    def test_basic_arithmetic_operations(self):
        # Functionalities 1: Perform Basic Arithmetic Operations
        self.assertEqual(self.calculator.perform_addition(5, 3), 8)
        self.assertEqual(self.calculator.perform_subtraction(7, -2), 9)
        self.assertEqual(self.calculator.perform_multiplication(4, 6), 24)
        self.assertEqual(self.calculator.perform_division(8, 2), 4)
        with self.assertRaises(ValueError):
            self.calculator.perform_division(10, 0)

    def test_calculate_square_roots(self):
        # Functionalities 2: Calculate Square Roots
        self.assertEqual(self.calculator.calculate_square_root(16), 4)
        self.assertEqual(self.calculator.calculate_square_root(0), 0)
        with self.assertRaises(ValueError):
            self.calculator.calculate_square_root(-9)

    def test_perform_exponentiation_calculations(self):
        # Functionalities 3: Perform Exponentiation Calculations
        self.assertEqual(self.calculator.perform_exponentiation(2, 3), 8)
        self.assertEqual(self.calculator.perform_exponentiation(0, 5), 0)
        self.assertEqual(self.calculator.perform_exponentiation(7, 0), 1)
        self.assertEqual(self.calculator.perform_exponentiation(-3, 2), 9)

    def test_calculate_percentages(self):
        # Functionalities 4: Calculate Percentages
        self.assertEqual(self.calculator.calculate_percentage(200, 10), 20)
        self.assertEqual(self.calculator.calculate_percentage(0, 25), 0)
        self.assertEqual(self.calculator.calculate_percentage(-50, 10), -5)

if __name__ == '__main__':
    unittest.main()
