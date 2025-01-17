import unittest
from main import CalculationAssistant

class TestCalculationAssistant(unittest.TestCase):

    def setUp(self):
        self.assistant = CalculationAssistant()

    def test_basic_arithmetic_operations(self):
        # Test addition
        self.assistant.input1 = "5"
        self.assistant.input2 = "3"
        self.assistant.operation = "add"
        self.assertEqual(self.assistant.perform_calculation(), 8)

        # Test subtraction
        self.assistant.input1 = "7"
        self.assistant.input2 = "-2"
        self.assistant.operation = "subtract"
        self.assertEqual(self.assistant.perform_calculation(), 9)

        # Test multiplication
        self.assistant.input1 = "4"
        self.assistant.input2 = "6"
        self.assistant.operation = "multiply"
        self.assertEqual(self.assistant.perform_calculation(), 24)

        # Test division
        self.assistant.input1 = "8"
        self.assistant.input2 = "2"
        self.assistant.operation = "divide"
        self.assertEqual(self.assistant.perform_calculation(), 4)

        # Test division by zero
        self.assistant.input1 = "10"
        self.assistant.input2 = "0"
        self.assistant.operation = "divide"
        with self.assertRaises(ZeroDivisionError):
            self.assistant.perform_calculation()

    def test_square_root(self):
        # Test square root of a positive number
        self.assistant.input1 = "16"
        self.assistant.operation = "square_root"
        self.assertEqual(self.assistant.perform_calculation(), 4)

        # Test square root of zero
        self.assistant.input1 = "0"
        self.assistant.operation = "square_root"
        self.assertEqual(self.assistant.perform_calculation(), 0)

        # Test square root of a negative number
        self.assistant.input1 = "-9"
        self.assistant.operation = "square_root"
        with self.assertRaises(ValueError):
            self.assistant.perform_calculation()

    def test_exponentiation(self):
        # Test exponentiation with positive base and exponent
        self.assistant.input1 = "2"
        self.assistant.input2 = "3"
        self.assistant.operation = "exponentiation"
        self.assertEqual(self.assistant.perform_calculation(), 8)

        # Test exponentiation with base zero and positive exponent
        self.assistant.input1 = "0"
        self.assistant.input2 = "5"
        self.assistant.operation = "exponentiation"
        self.assertEqual(self.assistant.perform_calculation(), 0)

        # Test exponentiation with positive base and zero exponent
        self.assistant.input1 = "7"
        self.assistant.input2 = "0"
        self.assistant.operation = "exponentiation"
        self.assertEqual(self.assistant.perform_calculation(), 1)

        # Test exponentiation with negative base and even exponent
        self.assistant.input1 = "-3"
        self.assistant.input2 = "2"
        self.assistant.operation = "exponentiation"
        self.assertEqual(self.assistant.perform_calculation(), 9)

    def test_percentage(self):
        # Test percentage calculation with positive number and percentage
        self.assistant.input1 = "200"
        self.assistant.input2 = "10"
        self.assistant.operation = "percentage"
        self.assertEqual(self.assistant.perform_calculation(), 20)

        # Test percentage calculation with zero and any percentage
        self.assistant.input1 = "0"
        self.assistant.input2 = "25"
        self.assistant.operation = "percentage"
        self.assertEqual(self.assistant.perform_calculation(), 0)

        # Test percentage calculation with negative number and percentage
        self.assistant.input1 = "-50"
        self.assistant.input2 = "10"
        self.assistant.operation = "percentage"
        self.assertEqual(self.assistant.perform_calculation(), -5)

if __name__ == '__main__':
    unittest.main()
