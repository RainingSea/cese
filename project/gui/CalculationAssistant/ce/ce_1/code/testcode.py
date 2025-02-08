import unittest
from main import CalculationAssistant

class TestCalculationAssistant(unittest.TestCase):

    def setUp(self):
        self.app = CalculationAssistant()
        self.app.root.withdraw()  # Hide the main window during tests

    def test_basic_arithmetic_operations(self):
        # Test addition
        self.app.input1.insert(0, '5')
        self.app.input2.insert(0, '3')
        self.app.perform_addition()
        self.assertEqual(self.app.result_label.cget("text"), "Addition: 8.0")

        # Test subtraction
        self.app.input1.delete(0, 'end')
        self.app.input2.delete(0, 'end')
        self.app.input1.insert(0, '7')
        self.app.input2.insert(0, '-2')
        self.app.perform_subtraction()
        self.assertEqual(self.app.result_label.cget("text"), "Subtraction: 9.0")

        # Test multiplication
        self.app.input1.delete(0, 'end')
        self.app.input2.delete(0, 'end')
        self.app.input1.insert(0, '4')
        self.app.input2.insert(0, '6')
        self.app.perform_multiplication()
        self.assertEqual(self.app.result_label.cget("text"), "Multiplication: 24.0")

        # Test division
        self.app.input1.delete(0, 'end')
        self.app.input2.delete(0, 'end')
        self.app.input1.insert(0, '8')
        self.app.input2.insert(0, '2')
        self.app.perform_division()
        self.assertEqual(self.app.result_label.cget("text"), "Division: 4.0")

        # Test division by zero
        self.app.input1.delete(0, 'end')
        self.app.input2.delete(0, 'end')
        self.app.input1.insert(0, '10')
        self.app.input2.insert(0, '0')
        self.app.perform_division()
        self.assertEqual(self.app.result_label.cget("text"), "Error: Division by zero")

    def test_calculate_square_roots(self):
        # Test square root of positive number
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '16')
        self.app.calculate_square_root()
        self.assertEqual(self.app.result_label.cget("text"), "Square Root: 4.0")

        # Test square root of zero
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '0')
        self.app.calculate_square_root()
        self.assertEqual(self.app.result_label.cget("text"), "Square Root: 0.0")

        # Test square root of negative number
        self.app.input1.delete(0, 'end')
        self.app.input1.insert(0, '-9')
        try:
            self.app.calculate_square_root()
            self.fail("Expected ValueError for negative input")
        except ValueError:
            pass

    def test_exponentiation_calculations(self):
        # Test exponentiation with positive base and exponent
        self.app.input1.delete(0, 'end')
        self.app.input2.delete(0, 'end')
        self.app.input1.insert(0, '2')
        self.app.input2.insert(0, '3')
        self.app.perform_exponentiation()
        self.assertEqual(self.app.result_label.cget("text"), "Exponentiation: 8.0")

        # Test exponentiation with base zero
        self.app.input1.delete(0, 'end')
        self.app.input2.delete(0, 'end')
        self.app.input1.insert(0, '0')
        self.app.input2.insert(0, '5')
        self.app.perform_exponentiation()
        self.assertEqual(self.app.result_label.cget("text"), "Exponentiation: 0.0")

        # Test exponentiation with exponent zero
        self.app.input1.delete(0, 'end')
        self.app.input2.delete(0, 'end')
        self.app.input1.insert(0, '7')
        self.app.input2.insert(0, '0')
        self.app.perform_exponentiation()
        self.assertEqual(self.app.result_label.cget("text"), "Exponentiation: 1.0")

        # Test exponentiation with negative base and even exponent
        self.app.input1.delete(0, 'end')
        self.app.input2.delete(0, 'end')
        self.app.input1.insert(0, '-3')
        self.app.input2.insert(0, '2')
        self.app.perform_exponentiation()
        self.assertEqual(self.app.result_label.cget("text"), "Exponentiation: 9.0")

    def test_calculate_percentages(self):
        # Test percentage calculation
        self.app.input1.delete(0, 'end')
        self.app.input2.delete(0, 'end')
        self.app.input1.insert(0, '200')
        self.app.input2.insert(0, '10')
        self.app.calculate_percentage()
        self.assertEqual(self.app.result_label.cget("text"), "Percentage: 20.0")

        # Test percentage calculation with zero
        self.app.input1.delete(0, 'end')
        self.app.input2.delete(0, 'end')
        self.app.input1.insert(0, '0')
        self.app.input2.insert(0, '25')
        self.app.calculate_percentage()
        self.assertEqual(self.app.result_label.cget("text"), "Percentage: 0.0")

        # Test percentage calculation with negative number
        self.app.input1.delete(0, 'end')
        self.app.input2.delete(0, 'end')
        self.app.input1.insert(0, '-50')
        self.app.input2.insert(0, '10')
        self.app.calculate_percentage()
        self.assertEqual(self.app.result_label.cget("text"), "Percentage: -5.0")

if __name__ == '__main__':
    unittest.main()
